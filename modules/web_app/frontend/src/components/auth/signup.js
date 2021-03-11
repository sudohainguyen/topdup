import { useRef } from "react"
import { Modal } from "react-bootstrap"
import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props'
import { GoogleLogin } from 'react-google-login'
import { FaFacebookSquare } from "react-icons/fa"
import { FcGoogle } from "react-icons/fc"
import ReactIconRender from "../../shared/react-icon-renderer"
import AuthService from "./auth-service"
import './auth.css'
import ValidatedSignupForm from "./vaidated-signup-form"

function SignupModal(props) {
  const mounted = useRef(true)
  const setUserData = props.setUserDa
  const authService = new AuthService()
  const onSubmitNomalSignup = (values) => {
    console.log(values)
  }

  const loginResponseHandler = (result, modalProps) => {
    const httpCode = result.code
    if (httpCode !== 200) throw (result.message)
    if (mounted.current) {
      setUserData(result.data)
      modalProps.onHide()
    }
  }

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
        <div className="layout-grid centered-container auth-heading"><h2>Đăng ký</h2></div>
        <div className="layout-grid centered-container margin-bottom--20">
          <GoogleLogin
            clientId="xxx"
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
          <ValidatedSignupForm onSubmitSignup={onSubmitNomalSignup} />
        </div>
      </div>
    </Modal>
  )
}

export default SignupModal
