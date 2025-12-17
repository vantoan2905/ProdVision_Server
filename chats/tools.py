# chats/tools.py
import io
import numpy as np
import easyocr
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

from sentence_transformers import SentenceTransformer
from mongoengine.queryset.visitor import Q
from langchain.tools import tool

from datetime import datetime
from typing import List, Dict, Any
from files.models import KnowledgeChunk

import random

# ======================================================
# Global singletons (performance optimization)
# ======================================================

EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
OCR_READER = easyocr.Reader(['en', 'vi'], gpu=True)


# ======================================================
# Utility functions
# ======================================================

def cosine_similarity(a, b) -> float:
    """
    Compute cosine similarity between two numeric vectors.

    Args:
        a (list | np.ndarray): First embedding vector.
        b (list | np.ndarray): Second embedding vector.

    Returns:
        float: Similarity score in range [-1, 1].
               Returns 0.0 if either vector is empty.
    """
    a = np.array(a)
    b = np.array(b)

    if a.size == 0 or b.size == 0:
        return 0.0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def _figure_to_tensor(fig) -> np.ndarray:
    """
    Convert a matplotlib figure into an RGB image tensor.

    The output tensor can be directly consumed by the client
    without saving the image to disk.

    Args:
        fig (matplotlib.figure.Figure): Matplotlib figure object.

    Returns:
        np.ndarray: Image tensor with shape (H, W, 3), dtype=uint8.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    image = plt.imread(buf)
    return (image[:, :, :3] * 255).astype(np.uint8)


# ======================================================
# OCR Tool
# ======================================================

@tool("ocr_tool")
def ocr_tool(img_path: str) -> str:
    """
    Extract text from an image using EasyOCR.

    Args:
        img_path (str): Path to the image file.

    Returns:
        str: Extracted text separated by newline characters.

    Notes:
        - Supports English and Vietnamese.
        - Returns text only, no image data.
    """
    results = OCR_READER.readtext(img_path)
    return "\n".join([text for _, text, _ in results])


# ======================================================
# Semantic Search Tool
# ======================================================

@tool("database_search")
def database_search(query: str, keyword: str = "", top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform semantic search over the MongoDB knowledge base.

    Args:
        query (str): Natural language query.
        keyword (str, optional): Keyword filter on title or text.
        top_k (int, optional): Number of top results to return.

    Returns:
        List[Dict[str, Any]]: Ranked search results, each containing:
            - score (float): Semantic similarity score.
            - title (str): Knowledge chunk title.
            - text (str): Knowledge chunk content.
            - metadata (dict): Additional metadata.
    """
    query_embedding = EMBED_MODEL.encode(query)

    chunks = KnowledgeChunk.objects(
        Q(title__icontains=keyword) |
        Q(text__icontains=keyword)
    ).limit(100)

    scored = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk.embedding)
        scored.append({
            "score": score,
            "title": chunk.title,
            "text": chunk.text,
            "metadata": chunk.metadata
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


# ======================================================
# Time Tool
# ======================================================

@tool("time")
def get_current_time() -> str:
    """
    Get the current server time.

    Returns:
        str: Current time formatted as 'HH:MM:SS'.
    """
    return datetime.now().strftime("%H:%M:%S")

# ======================================================
# Chart Tools (Matplotlib → Tensor)
# ======================================================


@tool("mock_time_series_data")
def mock_time_series_data(
    start: int = 1,
    end: int = 12,
    base_value: float = 1000.0,
    fluctuation: float = 300.0
) -> Dict[str, List]:
    """
    Generate mock time-series data for line charts.

    Args:
        start (int): Start index (e.g., month 1)
        end (int): End index (e.g., month 12)
        base_value (float): Base numeric value
        fluctuation (float): Maximum random fluctuation

    Returns:
        Dict[str, List]: {
            "labels": List[str] of x-axis labels,
            "values": List[float] of y-axis values
        }
    """
    labels = [str(i) for i in range(start, end + 1)]
    values = [base_value + random.uniform(-fluctuation, fluctuation) for _ in labels]
    return {"labels": labels, "values": values}


@tool("mock_category_data")
def mock_category_data(
    categories: List[str] = None,
    base_value: float = 1000.0,
    fluctuation: float = 300.0
) -> Dict[str, List]:
    """
    Generate mock category data for bar charts.

    Args:
        categories (List[str], optional): Category names. Default ["A", "B", "C"]
        base_value (float): Base numeric value
        fluctuation (float): Max random fluctuation

    Returns:
        Dict[str, List]: {
            "labels": category names,
            "values": list of numeric values
        }
    """
    if categories is None:
        categories = ["A", "B", "C"]

    values = [base_value + random.uniform(-fluctuation, fluctuation) for _ in categories]
    return {"labels": categories, "values": values}


@tool("mock_percentage_data")
def mock_percentage_data(
    categories: List[str] = None
) -> Dict[str, List]:
    """
    Generate mock percentage data for pie charts.

    Args:
        categories (List[str], optional): Category names. Default ["A", "B", "C", "D"]

    Returns:
        Dict[str, List]: {
            "labels": category names,
            "values": list of percentages summing to 100
        }
    """
    if categories is None:
        categories = ["A", "B", "C", "D"]

    raw = [random.uniform(1, 100) for _ in categories]
    total = sum(raw)
    values = [round(v / total * 100, 1) for v in raw]
    return {"labels": categories, "values": values}


# ================= CHART TOOLS (JSON OUTPUT) =================

@tool("draw_bar_chart")
def draw_bar_chart(
    labels: List[str],
    values: List[float],
    title: str = "Bar Chart",
    x_label: str = "",
    y_label: str = ""
) -> Dict[str, Any]:
    """
    Generate bar chart JSON data (for client-side rendering).

    Args:
        labels: List of category labels
        values: Numeric values
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        Dict[str, Any]: {
            "type": "bar",
            "title": title,
            "data": {
                "labels": labels,
                "values": values,
                "x_label": x_label,
                "y_label": y_label
            }
        }
    """
    return {
        "type": "bar",
        "title": title,
        "data": {
            "labels": labels,
            "values": values,
            "x_label": x_label,
            "y_label": y_label
        }
    }


@tool("draw_line_chart")
def draw_line_chart(
    labels: List[str],
    values: List[float],
    title: str = "Line Chart",
    x_label: str = "",
    y_label: str = ""
) -> Dict[str, Any]:
    """
    Generate line chart JSON data (for client-side rendering).

    Args:
        labels: Ordered x-axis labels
        values: Numeric y-axis values
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        Dict[str, Any]: {
            "type": "line",
            "title": title,
            "data": {
                "labels": labels,
                "values": values,
                "x_label": x_label,
                "y_label": y_label
            }
        }
    """
    return {
        "type": "line",
        "title": title,
        "data": {
            "labels": labels,
            "values": values,
            "x_label": x_label,
            "y_label": y_label
        }
    }


@tool("draw_pie_chart")
def draw_pie_chart(
    labels: List[str],
    values: List[float],
    title: str = "Pie Chart"
) -> Dict[str, Any]:
    """
    Generate pie chart JSON data (for client-side rendering).

    Args:
        labels: Category names
        values: Numeric values (percentage or raw)
        title: Chart title

    Returns:
        Dict[str, Any]: {
            "type": "pie",
            "title": title,
            "data": {
                "labels": labels,
                "values": values
            }
        }
    """
    return {
        "type": "pie",
        "title": title,
        "data": {
            "labels": labels,
            "values": values
        }
    }
