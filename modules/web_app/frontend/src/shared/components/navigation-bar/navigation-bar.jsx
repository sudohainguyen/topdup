import React from "react";
import "./navigation-bar.css";
import { Navbar, Nav, Container, NavDropdown } from "react-bootstrap";
import { useLocation } from "react-router-dom";

const NavigationBar = ({ isLogin }) => {
	const location = useLocation();

	return (
		<Navbar bg="primary" variant="dark" expand="lg" fixed="top">
			<Container>
				<Navbar.Brand href="/">TopDup</Navbar.Brand>
				<Navbar.Collapse id="basic-navbar-nav">
					<Nav className="mr-auto" activeKey={location.pathname}>
						<Nav.Link href="/sign-in">Home</Nav.Link>
						<Nav.Link href="/dupfinder">DupFinder</Nav.Link>
						<Nav.Link href="/dupviewer">DupViewer</Nav.Link>
						<Nav.Link href="/dupregister">DupRegister</Nav.Link>
					</Nav>
					<Nav>
						{isLogin ? (
							<>
								<NavDropdown
									title="User Dashboard"
									id="collasible-nav-dropdown"
								>
									<NavDropdown.Item href="#">Action</NavDropdown.Item>
									<NavDropdown.Item href="#">Another action</NavDropdown.Item>
									<NavDropdown.Item href="#">Something</NavDropdown.Item>
									<NavDropdown.Divider />
									<NavDropdown.Item href="#">Separated link</NavDropdown.Item>
								</NavDropdown>
								<Nav.Link href="#">Logout</Nav.Link>
							</>
						) : (
							<>
								<Nav.Link href="/sign-in">Sign In</Nav.Link>
								<Nav.Link href="/sign-up">Sign Up</Nav.Link>
							</>
						)}
					</Nav>
				</Navbar.Collapse>
			</Container>
		</Navbar>
	);
};

export default NavigationBar;
