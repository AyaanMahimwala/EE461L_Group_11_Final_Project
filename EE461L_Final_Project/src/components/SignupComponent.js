// signup.component.js
import { useState } from 'react'
import axios from "axios";

import Button from "@material-ui/core/Button";

import TextField from "@material-ui/core/TextField";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

const url = "http://localhost:5555/";

function handleSignup(signup_details, props) {
    let changeableUrl = `${url}api/signup_set/create`;
    let csrf = document.getElementsByName("csrf-token")[0].content;
    const request_content = {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        },
        credentials: "same-origin",
        body: JSON.stringify({ user_name: signup_details.username, user_password: signup_details.password, email: signup_details.email }),
    }
    axios.post(changeableUrl, request_content).then((result) => {
        console.log(result.data);
        props.setAuth(!props.auth);
        props.setOpenSignup(false);
    }, (error) => {
        console.log(error);
    })
};

function SignupComponent(props) {
    const [signup_details, setSignupDetails] = useState({ username: "", password: "", email: "" });
    const handleCloseSignup = () => {
        props.setOpenSignup(false);
    };
    const handleChange = e => {
        const { name, value } = e.target;
        setSignupDetails({ [name]: value })
        console.log(value)
    };
    return (
        <div>
            <Dialog
                open={props.open_signup}
                //onClose={handleCloseSignup}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">Signup</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Please enter the username, password and email you wish to sign up
                        with.
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="username"
                        required="true"
                        label="Username"
                        placeholder="Username"
                        type="text"
                        fullWidth
                        onChange={handleChange}
                    />
                    <TextField
                        margin="dense"
                        id="password"
                        required="true"
                        label="Password"
                        placeholder="Password"
                        type="password"
                        fullWidth
                        onChange={handleChange}
                    />
                    <TextField
                        margin="dense"
                        id="email"
                        required="true"
                        label="Email"
                        placeholder="Email"
                        type="email"
                        fullWidth
                        onChange={handleChange}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseSignup} color="primary">
                        Cancel
                </Button>
                    <Button onClick={handleSignup(signup_details, props)} color="primary">
                        Signup
                </Button>
                </DialogActions>
            </Dialog>
        </div>

    );
}

export default SignupComponent;
