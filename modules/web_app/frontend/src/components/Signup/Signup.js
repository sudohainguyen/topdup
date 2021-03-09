import { Button, Modal } from "react-bootstrap"

function SignupModal(props) {
  return (
    <Modal {...props} size="lg" aria-labelledby="contained-modal-title-vcenter">
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">Sign up</Modal.Title>
      </Modal.Header>
      <Modal.Body>Hello</Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Sign up</Button>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  )
}

export default SignupModal
