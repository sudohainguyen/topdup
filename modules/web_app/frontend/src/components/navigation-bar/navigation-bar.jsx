import React from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { useLocation, NavLink } from "react-router-dom";
import Authentication from "../auth/auth";
import "./navigation-bar.css";

const NavigationBar = (props) => {
  const location = useLocation();
  const logOut = () => {
    props.setUserData();
    window.location.assign("/");
  };

  return (
    <>
      <Navbar expand="lg" fixed="top">
        <Container>
          <Navbar.Brand className="topdup-brand" href="/">
            TopDup
          </Navbar.Brand>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto" activeKey={location.pathname}></Nav>
            <Nav className="topdup-nav-items">
              <NavLink to="/about" className="nav-link">
                Giới thiệu
              </NavLink>
              <NavLink to="/dup-report" className="nav-link">
                DupReport
              </NavLink>
              <NavLink to="/dup-compare" className="nav-link">
                DupCompare
              </NavLink>
              <Authentication />
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
};

export default NavigationBar;
