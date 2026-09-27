import { useState } from "react";
import { apiRequest } from "../api";

function Login({ onLogin, goRegister }) {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {

        e.preventDefault();

        setError("");
        setLoading(true);

        try {

            const data = await apiRequest("/login", {
                method: "POST",
                body: JSON.stringify({
                    username,
                    password
                })
            });

            localStorage.setItem("token", data.access_token);

            // JWT payload decode
            const payload = JSON.parse(
                atob(
                    data.access_token
                        .split(".")[1]
                        .replace(/-/g, "+")
                        .replace(/_/g, "/")
                )
            );

            localStorage.setItem("username", payload.sub);
            localStorage.setItem("role", payload.role);

            onLogin();

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

                    <p className="small-label">SMART INVENTORY SYSTEM</p>

                    <h1>
                        Manage your
                        <span> stuff smarter.</span>
                    </h1>

                    <p>
                        A simple and powerful product management
                        dashboard powered by FastAPI and React.
                    </p>

                    <div className="feature-list">
                        <div>✓ Secure JWT Authentication</div>
                        <div>✓ Role Based Access</div>
                        <div>✓ Fast Product Management</div>
                    </div>

                </div>

            </div>

            <div className="auth-right">

                <div className="auth-card">

                    <div className="mobile-brand">
                        <div className="brand-icon">✦</div>
                        HealthyStuff
                    </div>

                    <h2>Welcome back 👋</h2>

                    <p className="auth-subtitle">
                        Login to your account
                    </p>

                    {error && (
                        <div className="error-box">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleLogin}>

                        <label>Username</label>

                        <input
                            type="text"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />

                        <label>Password</label>

                        <input
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />

                        <button
                            className="primary-btn"
                            disabled={loading}
                        >
                            {loading ? "Signing in..." : "Sign In →"}
                        </button>

                    </form>

                    <p className="switch-text">
                        Don't have an account?
                        <button onClick={goRegister}>
                            Create account
                        </button>
                    </p>

                </div>

            </div>

        </div>
    );
}

export default Login;