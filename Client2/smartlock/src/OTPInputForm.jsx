import React, {Component} from 'react'
import { connect } from 'react-redux'
import axios from 'axios'
import lockimg from './latchlock.jpg'


class OTPInputForm extends Component {
  constructor(){
    super()
    this.state = {
      passcode: null,
      submitted: false,
      faceid:null,
      passcode_validation:false,
      visitor_name:null
    }
    this.submitHandler = this.submitHandler.bind(this)
    this.handleKeydown = this.handleKeydown.bind(this)
  }
  componentDidMount() {
      console.log('Input Form Mounted!')
  }
  handleKeydown = (e) => {
    //set passcode
    this.setState({ passcode: e.target.value })
  } 
  submitHandler = (e) => {
    e.preventDefault()
    const passcode = this.state.passcode
    console.log('passcode', passcode)

    //send passcode
    axios.post(`https://f3gii3hkr3.execute-api.us-east-1.amazonaws.com/Dev/passcodes`, { passcode, faceid: this.state.faceid })
        .then((res)=>{
          console.log(res.data)
          const { passcode_validation, visitor_name } = res.data.body
          this.setState({ submitted: true,  passcode_validation, visitor_name})
        })
  }
  render(){
    const faceid = this.props.location.search.slice(1).split('=')[1]
    this.state.faceid = faceid
    return (
      <div>
        <img src={lockimg} height="400px"/>
        { this.state.submitted === false &&
              (
              <form onSubmit={this.submitHandler}>
                <div className="container" style={{ margin: "auto", maxWidth: "250px", verticalAlign:"middle"}}>
                  <div style={{ padding:"10px" }}>
                    <label className="p-2">Enter OTP:</label>
                    <input id="passcode" name="passcode" className="form-control p-2" onChange={this.handleKeydown} placeholder="Enter OTP" />
                  </div>
                  <div className="form-group p-2">
                    <button className='btn btn-primary submitButton' onClick={this.submitHandler} >
                    Submit
                    </button>
                  </div>
                </div>
              </form>
              )
        }
        { this.state.submitted === true && this.state.passcode_validation === true &&
          (
            <div>
              <h3>Door Unlocked, Welcome {this.state.visitor_name}</h3>
            </div>
          )
        }
        { this.state.submitted === true && this.state.passcode_validation === false &&
          (
            <div>
              <h3>Invalid Passcode, {this.state.visitor_name} </h3>
              <em>Try Again Or Request A New One</em>
              <button className='btn btn-danger' 
              onClick={ ()=> this.setState({submitted:false}) }>
              Try Again</button>
            </div>
          )
        }
      </div>
    );
  }
}


export default OTPInputForm;
