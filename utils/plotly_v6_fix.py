import plotly
from packaging import version
import pandas as pd
import base64
import numpy as np
import plotly.graph_objects as go

# 1. Parse the installed Plotly version
PLOTLY_VERSION = version.parse(plotly.__version__)
IS_PLOTLY_V6_OR_NEWER = PLOTLY_VERSION >= version.parse("6.0.0")

def get_plotly_safe_data(df: pd.DataFrame, columns: list) -> dict | pd.DataFrame:
    """
    Returns a safe data structure for Plotly.
    - If Plotly v6+: Converts columns to native Python lists to bypass bdata serialization.
    - If Plotly v5-: Returns the standard DataFrame safely.
    """
    if IS_PLOTLY_V6_OR_NEWER:
        # Convert only the columns Plotly actually needs to reduce memory overhead
        return {col: df[col].tolist() for col in columns if col in df.columns}
    
    # If older plotly, return standard DataFrame
    return df


def clean_plotly_figure(fig):
    """
    Recursively scans and decodes any Plotly v6 binary 'bdata' blocks 
    back into standard Python lists. Streamlit can render this dictionary directly.
    """
    # 1. Convert Figure object to a standard Python dictionary
    if isinstance(fig, go.Figure):
        fig_dict = fig.to_dict()
    elif isinstance(fig, dict):
        fig_dict = fig
    else:
        return fig

    # 2. Map of Plotly's binary dtypes to NumPy dtypes
    dtype_map = {
        'f8': np.float64, 'float64': np.float64,
        'f4': np.float32, 'float32': np.float32,
        'i4': np.int32, 'int32': np.int32,
        'u4': np.uint32, 'uint32': np.uint32,
        'i2': np.int16, 'int16': np.int16,
        'u2': np.uint16, 'uint16': np.uint16,
        'i1': np.int8, 'int8': np.int8,
        'u1': np.uint8, 'uint8': np.uint8,
        'u1c': np.uint8, 'uint8c': np.uint8
    }

    def decode_recursive(node):
        if isinstance(node, dict):
            # If we find a bdata binary array block, decode it back to a list
            if 'bdata' in node and 'dtype' in node:
                try:
                    b64_str = node['bdata']
                    dtype_str = node['dtype']
                    np_dtype = dtype_map.get(dtype_str, np.float64)
                    
                    # Decode base64 bytes and read as a numpy array
                    raw_bytes = base64.b64decode(b64_str)
                    arr = np.frombuffer(raw_bytes, dtype=np_dtype)
                    
                    # Convert to normal list
                    return arr.tolist()
                except Exception:
                    return node
            
            # Continue checking other branches of the dict tree
            return {key: decode_recursive(value) for key, value in node.items()}
        
        elif isinstance(node, list):
            return [decode_recursive(item) for item in node]
        
        return node

    return decode_recursive(fig_dict)