import React, {Component} from 'react'
import { connect } from 'react-redux'
import axios from 'axios'


class NewVisitorForm extends Component {
  constructor(){
    super()
    this.state = {
      submitted: false,
      faceid:null,
      visitor_name:null,
      visitor_phone:null,
      approval_status: null,
    }
    this.submitHandler = this.submitHandler.bind(this)
    this.handleKeydown = this.handleKeydown.bind(this)
    this.handleReject = this.handleReject.bind(this)
  }
  componentDidMount() {
      console.log('Input Form Mounted!')
  }
  handleKeydown = (e) => {
    let { name, value} = e.target
    //Update name
    if(name==='visitor_name'){
      this.setState({ visitor_name: value }, ()=>console.log(this.state))
    }
    //Update Phone
    else if(name==='visitor_phone'){
      this.setState({ visitor_phone: value }, ()=>console.log(this.state))
    }
  } 
  submitHandler = (e) => {
    e.preventDefault()
    //send info
    this.state.approval_status = "approved"
    var {faceid, visitor_name, visitor_phone, approval_status} = this.state
    axios.post('https://f3gii3hkr3.execute-api.us-east-1.amazonaws.com/Dev/visitors',
      {
        faceid,
        approval_status,
        visitor_name,
        phone_number: visitor_phone
      }
    ).then( ()=> this.setState({submitted:true}) )
  }
  handleReject = (e) => {
      e.preventDefault()
      //send rejection
      this.state.approval_status = "denied"
      var {approval_status, faceid} = this.state
      axios.post('https://f3gii3hkr3.execute-api.us-east-1.amazonaws.com/Dev/visitors',
      {
        faceid,
        approval_status,
      }
    ).then( ()=> this.setState({submitted:true}) )
  }
  render(){
    const params = this.props.location.search.slice(1).split(/[=&]/)
    const faceid = params[1]
    const photo_url = params[3]
    this.state.faceid = faceid
    let {visitor_name, visitor_phone, submitted, approval_status} = this.state
    return (
      <div>
        <img src={photo_url} width="400" />
        { submitted === false &&
              (
              <form onSubmit={this.submitHandler}>
                <div className="form-group">
                  <label>Visitor Name</label>
                  <input id="name" name="visitor_name" className="form-control" onChange={this.handleKeydown} placeholder="Enter Full Name" style={{margin:"auto"}}/>
                </div>
                <div className="form-group">
                  <label>Visitor Phone Number</label>
                  <input id="phone" name="visitor_phone" className="form-control" onChange={this.handleKeydown} placeholder="Enter Phone Number"/>
                </div>
                <div className="form-group">
                  { (visitor_name && visitor_name.length>6) && (visitor_phone && visitor_phone.length>=10) &&
                    (
                      <button className='btn btn-success' onClick={this.submitHandler}>
                        Approve Visitor & Submit
                      </button>
                    )
                  }
                  { ((!visitor_name || visitor_name.length<6) || (!visitor_phone || visitor_phone.length<10)) &&
                    (
                      <div>
                        <button className='btn btn-dark' disabled>
                          Approve Visitor & Submit
                        </button>
                        <label>Input Length Too Short</label>
                      </div>
                    )
                  }
                  <div>
                    <button className='btn btn-danger' onClick={this.handleReject}>Reject Visitor</button>
                  </div>
                </div>
              </form>
              )
        }
        { submitted === true && approval_status === 'approved' &&
          (
            <div>
              <h3>Successfully Created Visitor & Sent OTP!</h3>
            </div>
          )
        }
        { submitted === true && approval_status === 'denied' &&
          (
            <div>
              <h3>Rejected User</h3>
            </div>
          )
        }
      </div>
    );
  }
}


export default NewVisitorForm;
