import 'bootstrap/dist/css/bootstrap.min.css'
import 'font-awesome/css/font-awesome.min.css'
import React, { useState } from "react"
import { BrowserRouter, Redirect, Route, Switch } from "react-router-dom"
import { ToastContainer } from 'react-toastify'
import useUserData from '../../shared/useUserData'
import { AuthContext } from '../auth/auth-context'
import Login from '../auth/login'
import Dashboard from '../dashboard'
import DupCompare from '../dup-compare/dup-compare'
import DupReport from '../dup-report/dup-report'
import Footer from '../footer/footer'
import NavigationBar from '../navigation-bar/navigation-bar'
import Preferences from '../preferences'

function App() {
  const { userData, setUserData } = useUserData()
  const token = userData && userData.accessToken

  const [loggedIn, setLoggedIn] = useState(false)
  const [user, setUser] = useState()

  const login = (user) => {
    setLoggedIn(true)
    setUser(user)
  }

  const logout = () => {
    setLoggedIn(false)
    setUser()
  }

  return (
    <AuthContext.Provider value={{ isLoggedIn: loggedIn, login: login, logout: logout, user: user }}>
      <BrowserRouter>
        <div className="App">
          <NavigationBar setUserData={setUserData} userData={userData} isLoggedIn={token ? true : false} />
          <div className="page-content">
            <Switch>
              <Redirect exact from="/" to="/dup-report" />
              <Route exact path="/sign-in" component={() => <Login setUserData={setUserData} />} />
              <Route exact path="/dashboard" component={Dashboard} />
              <Route exact path="/preferences" component={Preferences} />
              <Route exact path="/dup-compare" component={() => <DupCompare />} />
              <Route exact path="/dup-finder" component={() => <DupCompare />} />
              <Route exact path="/dup-report" component={() => <DupReport userData={userData} setUserData={setUserData} />} />
              <Route exact path="/dup-report/:id" component={() => <DupReport userData={userData} />} />
            </Switch>
          </div>
          {/* <ToastContainer
          position="bottom-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        /> */}
          {/* Same as */}
          <ToastContainer />
          <Footer />
        </div>
      </BrowserRouter>
    </AuthContext.Provider>
  )
}

export default App
