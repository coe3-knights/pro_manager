import React from 'react'
import Img from '../home/img'

import {ProjHead} from './Login'
import './Fpassword.css'
import {Link} from '@reach/router'

const emailRegex = RegExp(/^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)

class Fpassword extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            email : '',
            error : {
                email: ''
            }
        }
    }

    handleChange = (e) => {
        let {name, value} = e.target;
        let error = this.state.error;
        let state = this.state;
    }
    render(){
        const error = this.state.error
    return(
        <div className = 'm-wrapper'>
        <div className='main' ><Img /></div>
        <div className = 'f-wrapper'>
            <ProjHead />
            <p>Enter your email and we send you a password reset link.</p>
            <input 
                className = 'mail' 
                type = 'email'
                name = 'email'
                placeholder = 'Email'
                onChange = {this.handleChange}
            />
             {
                 error.firstName.length > 0 && (
                 <span className = "errorMessage"> {error.firstName}</span>
             )}
            <button 
                id = 'Btn2'
                onclick ={this.handleSubmit}>Send Request</button>
            <Link to = 'terms'>
               <p id = 'terms1'>Term of use. Privacy policy</p>
            </Link>
        </div>
        </div>
    )
}
}

export default Fpassword;