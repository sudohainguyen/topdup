import 'bootstrap/dist/css/bootstrap.min.css'
import 'font-awesome/css/font-awesome.min.css'
import React from "react"
import { BrowserRouter, Route, Switch } from "react-router-dom"
import useUserData from '../../shared/useUserData'
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

  return (
    <BrowserRouter>
      <div className="App">
        <NavigationBar setUserData={setUserData} isLoggedIn={token ? true : false} />
        <div className="page-content">
          <Switch>
            <Route exact path="/" component={() => !token ? <Login setUserData={setUserData} /> : <Dashboard />} />
            <Route exact path="/sign-in" component={() => <Login setUserData={setUserData} />} />
            <Route exact path="/dashboard" component={Dashboard} />
            <Route exact path="/preferences" component={Preferences} />
            <Route exact path="/dup-compare" component={() => <DupCompare />} />
            <Route exact path="/dup-finder" component={() => <DupCompare />} />
            <Route exact path="/dup-report" component={() => <DupReport userData={userData} />} />
            <Route exact path="/dup-report/:id" component={() => <DupReport userData={userData} />} />
          </Switch>
        </div>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App
