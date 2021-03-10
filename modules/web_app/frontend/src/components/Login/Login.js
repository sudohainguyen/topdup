import React, { useRef, useState } from "react"
import { Modal } from "react-bootstrap"
import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props'
import { GoogleLogin } from 'react-google-login'
import { FaFacebookSquare } from "react-icons/fa"
import { FcGoogle } from "react-icons/fc"
import ReactIconRender from "../../shared/components/React-Icon-Renderer"
import "./Login.css"
import AuthService from "./Login.service"


export default function LoginModal(props) {
  const [username, setUsername] = useState()
  const [password, setPassword] = useState()
  const setUserData = props.setUserData

  const mounted = useRef(true)
  const authService = new AuthService()

  const loginResponseHandler = (result, modalProps) => {
    const httpCode = result.code
    if (httpCode !== 200) throw (result.message)
    if (mounted.current) {
      setUserData(result.data)
      modalProps.onHide()
    }
  }

  const handleSubmit = async e => {
    e.preventDefault()
    authService.getToken({ username, password })
      .then(result => loginResponseHandler(result))
  }

  const fbLoginClicked = () => { }
  const fbLoginCallback = (fbRespose, modalProps) => {
    authService.loginByFacebook(fbRespose).then(
      result => loginResponseHandler(result, modalProps)
    )
  }

  const ggLoginCallback = (ggResponse) => {

  }

  return (
    <Modal {...props} aria-labelledby="contained-modal-title-vcenter">
      <div style={{ padding: "20px" }}>
        <div className="layout-grid centered-container"><h2>Đăng nhập</h2></div>
        <div className="layout-grid centered-container margin-bottom--20">
          <GoogleLogin
            clientId="658977310896-knrl3gka66fldh83dao2rhgbblmd4un9.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={ggLoginCallback}
            onFailure={ggLoginCallback}
            cookiePolicy={'single_host_origin'}
            render={renderProps => (
              <div onClick={renderProps.onClick}>
                <ReactIconRender className={'ext-login-btn'} color={'#4267B2'} IconComponent={FcGoogle} />
              </div>
            )}
          />
          <FacebookLogin style={{ 'margin-top': '-5px' }}
            appId="800436117349613"
            fields="name,email,picture"
            cssClass="btn btn-primary btn-block mt-2 ext-login-btn"
            callback={(response) => fbLoginCallback(response, props)}
            render={renderProps => (
              <div onClick={renderProps.onClick}>
                <ReactIconRender className={'ext-login-btn'} color={'#4267B2'} IconComponent={FaFacebookSquare} />
              </div>
            )}
          />
        </div>

        <div className="layout-grid centered-container margin-bottom--20">
          <form className="width--80">
            <div className="form-group">
              <input type="text" className="form-control" placeholder="Email"
                onChange={e => setUsername(e.target.value)} />
            </div>

            <div className="form-group">
              <input type="password" className="form-control" placeholder="Mật khẩu"
                onChange={e => setPassword(e.target.value)} />
            </div>

            <div className="form-group">
              <input type="password" className="form-control" placeholder="Mật khẩu"
                onChange={e => setPassword(e.target.value)} />
            </div>
            <div className="form-group">
              <button class="btn login-btn full-width" onClick={handleSubmit}>Đăng nhập</button>
            </div>
          </form>
        </div>

        <div className="layout-grid centered-container margin-bottom--20">
          Quên mật khẩu?
        </div>

        <div className="layout-grid centered-container margin-bottom--20">
          Chưa có tài khoản?  <a href="#"> Đăng ký</a>
        </div>
      </div>
    </Modal>
  )
}

