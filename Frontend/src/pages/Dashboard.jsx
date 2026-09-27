import { useEffect, useState } from "react";
import { apiRequest } from "../api";

import Navbar from "../components/Navbar";
import ProductCard from "../components/ProductCard";
import ProductModal from "../components/ProductModal";

function Dashboard({ onLogout }) {

    const [products, setProducts] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [showModal, setShowModal] = useState(false);

    const [editingProduct, setEditingProduct] = useState(null);

    const username = localStorage.getItem("username");
    const role = localStorage.getItem("role");

    const isAdmin = role === "admin";

    const loadProducts = async () => {

        try {

            setLoading(true);
            setError("");

            const data = await apiRequest("/stuff");

            setProducts(data.Stuff || []);

        } catch (err) {

            setError(err.message);

            if (
                err.message.includes("authentication") ||
                err.message.includes("credentials")
            ) {
                onLogout();
            }

        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadProducts();
    }, []);

    const handleAdd = async (product) => {

        try {

            await apiRequest("/stuff", {
                method: "POST",
                body: JSON.stringify(product)
            });

            setShowModal(false);

            await loadProducts();

        } catch (err) {
            alert(err.message);
        }
    };

    const handleUpdate = async (product) => {

        try {

            await apiRequest(`/stuff/${editingProduct.id}`, {
                method: "PUT",
                body: JSON.stringify(product)
            });

            
            await loadProducts();
            setShowModal(false);
            setEditingProduct(null);

        } catch (err) {
            alert(err.message);
        }
    };

    const handleDelete = async (id) => {

        const confirmDelete = window.confirm(
            "Are you sure you want to delete this product?"
        );

        if (!confirmDelete) return;

        try {

            await apiRequest(`/stuff/${id}`, {
                method: "DELETE"
            });

            await loadProducts();

        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="dashboard">

            <Navbar
                username={username}
                role={role}
                onLogout={onLogout}
            />

            <main className="dashboard-content">

                <div className="welcome-section">

                    <div>

                        <p className="small-label">
                            DASHBOARD
                        </p>

                        <h1>
                            Take Stuff and Live Healthy
                        </h1>

                        <p>
                            Enjoy your best moment of your life 🍾
                        </p>

                    </div>

                    {isAdmin && (
                        <button
                            className="add-product-btn"
                            onClick={() => {
                                setEditingProduct(null);
                                setShowModal(true);
                            }}
                        >
                            + Add Product
                        </button>
                    )}

                </div>

                <div className="stats">

                    <div className="stat-card">

                        <div className="stat-icon">
                            📦
                        </div>

                        <div>
                            <span>Total Products</span>
                            <strong>{products.length}</strong>
                        </div>

                    </div>

                    <div className="stat-card">

                        <div className="stat-icon">
                            👤
                        </div>

                        <div>
                            <span>Logged in as</span>
                            <strong>{role}</strong>
                        </div>

                    </div>

                    <div className="stat-card">

                        <div className="stat-icon">
                            🔐
                        </div>

                        <div>
                            <span>Access</span>
                            <strong>
                                {isAdmin
                                    ? "Admin"
                                    : "User"}
                            </strong>
                        </div>

                    </div>

                </div>

                <div className="products-section">

                    <div className="section-heading">

                        <div>
                            <h2>Products</h2>

                            <p>
                                {isAdmin
                                    ? "Create, update and delete products."
                                    : "Browse available products."}
                            </p>
                        </div>

                        <button
                            className="refresh-btn"
                            onClick={loadProducts}
                        >
                            ↻ Refresh
                        </button>

                    </div>

                    {error && (
                        <div className="error-box">
                            {error}
                        </div>
                    )}

                    {loading ? (

                        <div className="loading">
                            <div className="spinner"></div>
                            Loading products...
                        </div>

                    ) : products.length === 0 ? (

                        <div className="empty-state">

                            <div>📦</div>

                            <h3>
                                No products found
                            </h3>

                            <p>
                                There are no products
                                available right now.
                            </p>

                            {isAdmin && (
                                <button
                                    className="primary-btn small"
                                    onClick={() => setShowModal(true)}
                                >
                                    Add your first product
                                </button>
                            )}

                        </div>

                    ) : (

                        <div className="products-grid">

                            {products.map((product) => (

                                <ProductCard
                                    key={product.id}
                                    product={product}
                                    isAdmin={isAdmin}
                                    onEdit={(product) => {
                                        setEditingProduct(product);
                                        setShowModal(true);
                                    }}
                                    onDelete={handleDelete}
                                />

                            ))}

                        </div>

                    )}

                </div>

            </main>

            {showModal && (
                <ProductModal
                    product={editingProduct}
                    onClose={() => {
                        setShowModal(false);
                        setEditingProduct(null);
                    }}
                    onSave={
                        editingProduct
                            ? handleUpdate
                            : handleAdd
                    }
                />
            )}

        </div>
    );
}

export default Dashboard;