function ProductCard({
    product,
    isAdmin,
    onEdit,
    onDelete
}) {

    return (
        <div className="product-card">

            <div className="product-top">

                <div className="product-icon">
                    📦
                </div>

                <span className="product-id">
                    #{product.id}
                </span>

            </div>

            <h3>{product.name}</h3>

            <div className="price">
                ₹{product.price}
            </div>

            <div className="product-footer">

                <span className="stock">
                    ● Available
                </span>

                {isAdmin && (
                    <div className="admin-actions">

                        <button
                            className="edit-btn"
                            onClick={() => onEdit(product)}
                        >
                            Edit
                        </button>

                        <button
                            className="delete-btn"
                            onClick={() => onDelete(product.id)}
                        >
                            Delete
                        </button>

                    </div>
                )}

            </div>

        </div>
    );
}

export default ProductCard;