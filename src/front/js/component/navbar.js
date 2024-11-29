import React from "react";
import { Link, Navigate } from "react-router-dom";
import { useParams, useNavigate } from 'react-router-dom';

export const Navbar = () => {
	const navigate = useNavigate();
	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">Login</span>
				</Link>
				<div className="ml-auto">
					<Link to="/demo">
						<button className="btn btn-primary" onClick={() => {Navigate("/demo")}}>Clickeame para ingresar a una pagina privada</button>
					</Link>
				</div>
			</div>
		</nav>
	);
};
