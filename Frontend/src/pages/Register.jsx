import { useState } from "react";
import { apiRequest } from "../api";

function Register({ goLogin }) {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const [loading, setLoading] = useState(false);

    const handleRegister = async (e) => {

        e.preventDefault();

        setError("");
        setSuccess("");
        setLoading(true);

        try {

            const data = await apiRequest("/register", {
                method: "POST",
                body: JSON.stringify({
                    username,
                    password
                })
            });

            setSuccess(data.message);

            setUsername("");
            setPassword("");

            setTimeout(() => {
                goLogin();
            }, 1200);

        } catch (err) {
            setError(err.message);
        }

        setLoading(false);
    };

    return (
        <div className="auth-page">

            <div className="auth-left">

                <div className="brand">
                    <div className="brand-icon">✦</div>
                    <span>HealthyStuff</span>
                </div>

                <div className="hero-content">

                    <p className="small-label">
                        CREATE YOUR ACCOUNT
                    </p>

                    <h1>
                        Start managing
                        <span> products today.</span>
                    </h1>

                    <p>
                        Create your account and access your
                        personalized product dashboard.
                    </p>

                </div>

            </div>

            <div className="auth-right">

                <div className="auth-card">

                    <div className="mobile-brand">
                        <div className="brand-icon">✦</div>
                        HealthyStuff
                    </div>

                    <h2>Create account 🚀</h2>

                    <p className="auth-subtitle">
                        Register a new account
                    </p>

                    {error && (
                        <div className="error-box">
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className="success-box">
                            {success}
                        </div>
                    )}

                    <form onSubmit={handleRegister}>

                        <label>Username</label>

                        <input
                            type="text"
                            placeholder="Choose username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />

                        <label>Password</label>

                        <input
                            type="password"
                            placeholder="Create password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />

                        <button
                            className="primary-btn"
                            disabled={loading}
                        >
                            {loading ? "Creating..." : "Create Account →"}
                        </button>

                    </form>

                    <p className="switch-text">
                        Already have an account?
                        <button onClick={goLogin}>
                            Login
                        </button>
                    </p>

                </div>

            </div>

        </div>
    );
}

export default Register;