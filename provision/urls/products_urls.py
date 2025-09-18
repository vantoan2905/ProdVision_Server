from django.urls import path

from provision.views.product_views import (
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView
)

base_urls = "products"
"""
| Endpoint              | Method    | Mô tả                  | Input                              | Output                 |
| --------------------- | --------- | ---------------------- | ---------------------------------- | ---------------------- |
| `/api/products/`      | GET       | Lấy danh sách sản phẩm | Query: category                    | List of products       |
| `/api/products/`      | POST      | Thêm sản phẩm mới      | JSON: `{name, category_id, batch}` | Product object created |
| `/api/products/<id>/` | GET       | Chi tiết sản phẩm      | -                                  | Product object         |
| `/api/products/<id>/` | PUT/PATCH | Cập nhật sản phẩm      | JSON: fields cần update            | Product object updated |
| `/api/products/<id>/` | DELETE    | Xóa sản phẩm           | -                                  | Status 204             |

"""
urlpatterns = [
    path(f"{base_urls}/", ProductListView.as_view(), name="product_list"),
    path(f"{base_urls}/", ProductCreateView.as_view(), name="product_create"),
    path(f"{base_urls}/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path(f"{base_urls}/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path(f"{base_urls}/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
]

