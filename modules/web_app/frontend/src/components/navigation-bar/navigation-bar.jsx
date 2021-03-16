import React from "react"
import { Container, Nav, Navbar } from "react-bootstrap"
import { useLocation } from "react-router-dom"
import Authentication from "../auth/auth"
import "./navigation-bar.css"

const NavigationBar = (props) => {
  const location = useLocation()
  const logOut = () => {
    props.setUserData()
    window.location.assign("/")
  }

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
              <Nav.Link href="/home">Trang chủ</Nav.Link>
              <Nav.Link href="/dup-report">Dup Reports</Nav.Link>
              <Nav.Link href="/dup-check">Dup Compare</Nav.Link>
              <Nav.Link href="/dup-finder">Dup Finder</Nav.Link>
              <Nav.Link href="/about">Về TopDup</Nav.Link>
              <Authentication />
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}

export default NavigationBar
