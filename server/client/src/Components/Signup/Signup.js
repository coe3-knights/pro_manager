import React from 'react'
import '../ionicons-2.0.1/css/ionicons.min.css'
import './Signup.css'
import { Link, navigate} from '@reach/router'
import axios from 'axios';
import Img from '../home/img'

 
const emailRegex = RegExp(/^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)

const formValid = ({formErrors, ...rest}) => {
    let valid = true;

    Object.values(formErrors).forEach(val => {
        val.length > 0 && (valid = false);
    });

    Object.values(rest).forEach(val => {
        val === null && (valid = false);
    });

    return valid;
};

export class Signup extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            id: 1,
            firstName: null,
            lastName: null,
            userName: null,
            email: null,
            password: null,
            confirmPassword: null,
            school: 'K N U S T',
            department: 'COMPUTER',
            isStudent: true,
            isLecture: false,
            formErrors: {
                firstName: '',
                lastName: '',
                userName: '',
                email: '',
                password: '',
                confirmPassword: '',
                // school: '',
                // department: ''
                
            }
        };
    }

    //When forms is submitted
    handleSubmit = e => {
        const state = this.state;
        e.preventDefault();
        if(formValid(this.state)){
            navigate("/dashboard")

        axios.post('http://localhost:3000/user', state)
        .then(function(response){
            //handle success
            console.log(response);
        })
        .catch(function(error) {
            //handle error
            console.log(error);
        });
        }

        else{
            alert('Please complete form')
        }

    }
//Handles event in the form

    handleStatChange = e => {

        e.preventDefault()
       if(e.target.id === 'isStudent'){
           this.setState({
               isStudent: true,
               isLecture: false
           })
        }
           else if(e.target.id === 'isLecturer'){
               this.setState({
                   isLecture: true,
                   isStudent: false

               })
           }
       
    }

    handleChange = e => {
        e.preventDefault();
        const {name, value} = e.target;
        let formErrors = this.state.formErrors;
        let state = this.state;


        switch(name){
            case 'firstName':
               formErrors.firstName = 
               value.length < 3 ? '*minimum of 3 characters required' : '';
               break;

            case 'lastName':
               formErrors.lastName = 
               (value.length >= 3) ? "" : "*minimum of 3 characters required" ;
               break;

            case 'userName':
              formErrors.userName = 
              value.length < 3 ? "*minimum of 3 characters requried" : "";
              break;

            case 'email':
                formErrors.email = 
                emailRegex.test(value) && value.length > 0 ? "" : "*invalid Email Address";
                break;

            case 'password':
               formErrors.password = 
               value.length < 6 ? "*minimum of 6 characters required" : "";
               break;
            
            case 'confirmPassword':
                 formErrors.confirmPassword = 
                 value === state.password ? "" : "*Password Mismatch";
                 break;

            // case 'school':
            //     formErrors.school = 
            //     value.length < 4 ? "*invalid entry" : '';
            //     break;

            // case 'department':
            //     formErrors.department =
            //     value.length < 3 ? '*minimum of 3 characters required' : '';
            //     break;

            default:
                break;
           

        }
        this.setState({ formErrors, [name]: value}, () => console.log(this.state)); 
    }

  
    render() 
    { 
        const ProjHead = ()=> {
            return(
                <div id = "head">
                    <h1 className= 'head'>KNIGHTS  PROJECT
                       <br />
                       <span>MANAGER</span>
                    </h1>
                </div>
            )
        }
        const {formErrors} = this.state;
       
        return (   

            <div className = 'wrapper'>
             <div className='main' ><Img /></div>
            <div className = 'form-wrapper'>
              <ProjHead />
              <p>Please complete to create your account.</p>
              <div className = 'forms'>
                    <form onSubmit = {this.handleSubmit} noValidate >
                      <div className = "firstName">       
                            <input
                                type = 'text'
                                className = {(formErrors.firstName.length > 0) ? "error" : null}
                                placeholder = 'First Name'
                                name = 'firstName'
                                noValidate
                                onChange = {this.handleChange}
                            />
                          
                            {
                                formErrors.firstName.length > 0 && (
                                <span className = "errorMessage"> {formErrors.firstName}</span>
                            )}
                        </div>
                        <div className = "lastName">
                            
                            <input
                                type = 'text'
                                className = {(formErrors.lastName.length > 0) ? "error" : null}
                                placeholder = 'Last Name'
                                name = 'lastName'
                                noValidate
                                onChange = {this.handleChange}
                            />
                           
                            {formErrors.lastName.length > 0 && (
                              <span className = "errorMessage">{formErrors.lastName}</span>
                            )} 
                        </div>

                        <div className = "userName">
                           
                            <input
                                type = 'text'
                                className = {(formErrors.userName.length > 0) ? "error" : null}
                                placeholder = 'User Name'
                                name = 'userName'
                                noValidate
                                onChange = {this.handleChange}
                            />
                            
                            {formErrors.userName.length > 0 && (
                              <span className = "errorMessage">{formErrors.userName}</span>
                            )} 
                        </div>

                        <div className = "email">
                            
                            <input
                                className = {formErrors.email.length > 0 ? "error" : null}
                                placeholder = 'Email'
                                type = 'email'
                                name = 'email'
                                noValidate
                                onChange = {this.handleChange}
                            />

                            {formErrors.email.length > 0 && (
                                <span className = "errorMessage">{formErrors.email}</span>
                              )}

                        </div>
                        <div className = "password">
                            
                            <input
                                className = {formErrors.password.length > 0 ? "error" : null}
                                placeholder = 'Password'
                                type = 'password'
                                name = 'password'
                                noValidate
                                onChange = {this.handleChange}
                            />
                          
                            
                            {formErrors.password.length > 0 && (
                              <span className = "errorMessage">{formErrors.password}</span>
                              )}

                        </div>

                        <div className = "Cpassword">
                            
                            <input
                                className = {formErrors.confirmPassword.length > 0 ? "error" : null}
                                placeholder = 'Confirm Password'
                                type = 'password'
                                name = 'confirmPassword'
                                noValidate
                                onChange = {this.handleChange}
                            />
                            
                            
                            {formErrors.password.length > 0 && (
                              <span className = "errorMessage">{formErrors.confirmPassword}</span>
                              )}

                        </div>

                        <div className = "School">
                        <select
                        name= 'school'
                        onChange = {this.handleChange}>
                            <option>{this.state.school}</option>
                        </select>
                        </div>

                        
                        <div className = "Department">
                           <select
                           name= 'department'
                           onChange = {this.handleChange}>
                               <option>COMPUTER</option>
                               <option>ELECTRICAL</option>
                               <option>TELECOM</option>
                               <option>BIOMED</option>
                           </select>

                        </div>
 
                            <div className = 'stat' >
                                <input 
                                className = 'status'
                                type = 'radio' 
                                id = 'isStudent'
                                name = 'status'
                                defaultChecked
                                 value = {this.state.isStudent}
                                 onChange = {this.handleStatChange}
                                />
                                <label id = "l0" htmlFor = 'isStudent'>Student</label>

                                
                                <input 
                                className = 'status'
                                type = 'radio'
                                id = 'isLecturer'
                                name = 'status'
                                 value = {this.state.isLecture}
                                 onChange = {this.handleStatChange}
                                />
                                <label id = "l1" htmlFor = 'isLecturer'>Lecturer</label>
                            </div>

                            <Link to = '/login'>
                            <p id = "acc"> Already Have an Account?</p>
                          </Link>
   
                        <div className = 'createAccount'>
                            <button className = 'ca-btn'>Create Account</button>    
                        </div>
                          <Link to = 'terms'>
                            <p id = 'terms1'>Term of use. Privacy policy</p>
                         </Link> 
                    </form>
                    </div>
                </div>
            </div>
         );
    }
}
 
export default Signup;