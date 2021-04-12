// login.component.js
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

function handleLogin(login_details, props) {
    let changeableUrl = `${url}api/login_set/validate`;
    let csrf = document.getElementsByName("csrf-token")[0].content;
    const request_content = {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        },
        credentials: "same-origin",
        body: JSON.stringify({ user_name: login_details.username, user_password: login_details.password }),
    }
    axios.post(changeableUrl, request_content).then((result) => {
        console.log(result.data);
        props.setAuth(!props.auth);
        props.setOpenLogin(false);
    }, (error) => {
        console.log(error);
    })
};

function LoginComponent(props) {
    const [login_details, setLoginDetails] = useState({ username: "", password: "" });
    const handleCloseLogin = () => {
        props.setOpenLogin(false);
    };

    const handleChange = e => {
        const { name, value } = e.target;
        setLoginDetails({ [name]: value })
    };
    return (
        <div>
            <Dialog
                open={props.open_login}
                //onClose={handleCloseLogin}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">Login or Signup</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        To login please enter the username and password you signed up
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
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseLogin} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleLogin(login_details, props)} color="primary">
                        Login
                    </Button>
                </DialogActions>
            </Dialog>
        </div>

    );
}

export default LoginComponent;
