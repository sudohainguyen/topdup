import "./App.css";
import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import Dashboard from "../Dashboard/Dashboard";
import Preferences from "../Preferences/Preferences";
import Login from "../Login/Login";
import useToken from "./useToken";
import NavigationBar from "../../shared/components/navigation-bar/navigation-bar";

function App() {
	const { token, setToken } = useToken();
	const [isLogin, setIsLogin] = React.useState(true);

	React.useEffect(() => {
		token ? setIsLogin(true) : setIsLogin(false);
	}, [token]);

	return (
		<BrowserRouter>
			<div className="App">
				<NavigationBar isLogin={isLogin} />

				<div className="auth-wrapper">
					<div className="auth-inner">
						<Switch>
							<Route
								exact
								path="/"
								component={() => {
									return !token ? <Login setToken={setToken} /> : <Dashboard />;
								}}
							/>
							<Route exact path="/dashboard" component={Dashboard} />
							<Route exact path="/Preferences" component={Preferences} />
						</Switch>
					</div>
				</div>
			</div>
		</BrowserRouter>
	);
}

export default App;
