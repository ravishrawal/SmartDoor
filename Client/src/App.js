import './App.css';
import OTPInputForm from './OTPInputForm'
import NewVisitorForm from './NewVisitorForm'
import React, {Component} from 'react'
import {Route, BrowserRouter} from 'react-router-dom'


class App extends Component {
  
  componentDidMount() {
      console.log('Mounted!')
  }
  render(){
    console.log(this.props)
    return (
      <div className="App" >
        <header className="App-header">
        </header>
        <BrowserRouter>
          <Route path="/passcode" component={OTPInputForm} />
          <Route path="/visitors/new" component={NewVisitorForm} />
        </BrowserRouter>
      </div>
    );
  }
}


export default App;
