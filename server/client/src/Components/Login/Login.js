import React from 'react'
import {Link} from '@reach/router'
import '../ionicons-2.0.1/css/ionicons.min.css'
import '../Login/newLogin.css'
import Img from '../home/img'
// import Axios from 'axios';


export function ProjHead(){
    return(
        <div id = "signtext">
            <h1 className= 'signtext'>KNIGHTS  PROJECT
               <br />
               <span>MANAGER</span>
            </h1>
        </div>
    )
}

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            username: '',
            password: ''
         }
         this.handleChange = this.handleChange.bind(this)
         this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(e){
        e.preventDefault();

        // alert('Hi ' + this.state.username + ' your password is ' + this.state.password)        
    }

    handleChange(e){
        const target = e.target;
        const name = target.name;
        if(name === 'username'){
            this.setState({
                username: target.value
            })
        }
        else if(name === 'password'){
            this.setState({
                password: target.value
            })
        }
    }
   
    
    render() { 
       
        const username = this.state.username;
        const password = this.state.password;

        return ( 
            <div className='main_wrapper'>
            <div className='main' ><Img /></div>
               <div className = 'forms_wrapper'>
               <ProjHead />
              <p id = 'text'>Welcome! Please login to your account.</p>
            <div className = 'wrap'>
            <form 
            className = 'log_in'
            onSubmit = {this.handleSubmit} >
              <label className = 'ion-android-person person' />
                <input
                 className = ' user_name' 
                 type = 'text'
                 name = 'username'
                 placeholder = 'Username'
                 value = {username}
                 onChange = {this.handleChange}
                 />
                {/* <label className = 'label1'
                       htmlFor = 'username'>Username</label> */}
               
                <input
                 className = 'pass_word' 
                 type = 'text'
                 name = 'password'
                 placeholder = 'Password'
                 value = {password}
                 onChange = {this.handleChange}
                 />
                 
                  {/* <label className = 'label2'
                   htmlFor = 'password'>Password</label> */}
                
                <div className = 'detail'>
                <input 
                  type = 'checkbox'
                  className = 'checkbox'
                  />
                  <span id = 'rem'>Remember me</span>
                <Link to = '/fpassword'>
                  <span id = "f_password">Forgot_Password</span>
                </Link>
                </div>
                
               <div className = 'btn1'>
                   <button className = 'submit_1'>Login</button>

               </div>
                <Link to = 'term'>
                    <p id = 'term'>Term of use. Privacy policy</p>
                </Link>
            </form>
            </div>
               </div>
            </div>
         );
    }
}
 
export default Login;