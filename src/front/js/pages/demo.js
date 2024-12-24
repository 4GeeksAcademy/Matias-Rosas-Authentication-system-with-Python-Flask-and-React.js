import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";

import { Context } from "../store/appContext";

export const Demo = () => {
	const { store, actions } = useContext(Context);
	const [error, setError] = useState("");
  	const [success, setSuccess] = useState("");

	const CheckToken = () => {
		const token = localStorage.getItem('jwt-token')
		console.log("El token: ",token)
		fetch(`${process.env.BACKEND_URL}/private`, {
			method: 'GET',
			headers: {
				"Content-Type": "application/json",
				'Authorization': `Bearer ${token}`
			}
		})
			.then((resp)=>{
				console.log(resp.ok)
				console.log(resp.status)
				console.log(resp.body)
				if (!resp.ok) {
				  if (resp.status === 400) {
					setError("Invalid access");
				  } else {
					setError("You shall not pass");
				  }
				  setSuccess("");
				  return null
				}
				return resp.json(); // Convertir a JSON solo si no hubo error
			})
			.then((data)=> {
				console.log("La data que vino: ", data)
				if (!data){
					return;
				}
				setError("");
        		setSuccess("You can access");
			})
			.catch((error) => {
				console.error("Error:", error.message);
			  });
	}


	useEffect(() => {
        CheckToken()
    }, []);
	
	return (
		<div className="container">
			<h1>Esta es una pagina privada 🔒</h1>
			{error && <div className="alert alert-danger mt-3">{error}</div>}
			{success && <div className="alert alert-success mt-3">{success}</div>}
			<br />
			<Link to="/Home">
				<button className="btn btn-primary">Back home</button>
			</Link>
		</div>
	);
};
