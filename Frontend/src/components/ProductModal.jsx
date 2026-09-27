import { useEffect, useState } from "react";

function ProductModal({
    product,
    onClose,
    onSave
}) {

    const [id, setId] = useState("");
    const [name, setName] = useState("");
    const [price, setPrice] = useState("");

    useEffect(() => {

        if (product) {
            setId(product.id);
            setName(product.name);
            setPrice(product.price);
        } else {
            setId("");
            setName("");
            setPrice("");
        }

    }, [product]);

    const submit = (e) => {

        e.preventDefault();

        onSave({
            id: Number(id),
            name,
            price: Number(price)
        });
    };

    return (
        <div className="modal-overlay">

            <div className="modal">

                <div className="modal-header">

                    <div>
                        <p className="small-label">
                            PRODUCT
                        </p>

                        <h2>
                            {product
                                ? "Edit Product"
                                : "Add Product"}
                        </h2>
                    </div>

                    <button
                        className="close-btn"
                        onClick={onClose}
                    >
                        ×
                    </button>

                </div>

                <form onSubmit={submit}>

                    <label>Product ID</label>

                    <input
                        type="number"
                        value={id}
                        onChange={(e) => setId(e.target.value)}
                        required
                    />

                    <label>Product Name</label>

                    <input
                        type="text"
                        placeholder="e.g. Protein Bar"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />

                    <label>Price</label>

                    <input
                        type="number"
                        placeholder="Enter price"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        required
                    />

                    <div className="modal-actions">

                        <button
                            type="button"
                            className="cancel-btn"
                            onClick={onClose}
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            className="primary-btn"
                        >
                            {product
                                ? "Update Product"
                                : "Create Product"}
                        </button>

                    </div>

                </form>

            </div>

        </div>
    );
}

export default ProductModal;