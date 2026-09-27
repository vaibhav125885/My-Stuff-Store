function Navbar({ username, role, onLogout }) {

    return (
        <nav className="navbar">

            <div className="nav-brand">
                <div className="brand-icon">✦</div>
                <span>HealthyStuff</span>
            </div>

            <div className="nav-right">

                <div className="user-info">

                    <div className="avatar">
                        {username?.charAt(0).toUpperCase()}
                    </div>

                    <div>
                        <strong>{username}</strong>

                        <small>
                            {role === "admin"
                                ? "Administrator"
                                : "User"}
                        </small>
                    </div>

                </div>

                <button
                    className="logout-btn"
                    onClick={onLogout}
                >
                    Logout
                </button>

            </div>

        </nav>
    );
}

export default Navbar;