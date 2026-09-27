import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

function App() {

    const [page, setPage] = useState(
        localStorage.getItem("token") ? "dashboard" : "login"
    );

    const handleLogin = () => {
        setPage("dashboard");
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        localStorage.removeItem("role");

        setPage("login");
    };

    if (page === "login") {
        return (
            <Login
                onLogin={handleLogin}
                goRegister={() => setPage("register")}
            />
        );
    }

    if (page === "register") {
        return (
            <Register
                goLogin={() => setPage("login")}
            />
        );
    }

    return (
        <Dashboard
            onLogout={handleLogout}
        />
    );
}

export default App;