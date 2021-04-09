import React from "react";
import clsx from "clsx";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import IconButton from "@material-ui/core/IconButton";
import Button from "@material-ui/core/Button";
import MenuIcon from "@material-ui/icons/Menu";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import InboxIcon from "@material-ui/icons/MoveToInbox";
import MailIcon from "@material-ui/icons/Mail";
import AccountCircle from "@material-ui/icons/AccountCircle";
import MenuItem from "@material-ui/core/MenuItem";
import Menu from "@material-ui/core/Menu";

import DnsRoundedIcon from "@material-ui/icons/DnsRounded";
import SettingsEthernetIcon from "@material-ui/icons/SettingsEthernet";
import AccountBalanceWalletIcon from "@material-ui/icons/AccountBalanceWallet";
import AssessmentIcon from "@material-ui/icons/Assessment";
import DesktopWindowsIcon from "@material-ui/icons/DesktopWindows";
import BookmarksIcon from "@material-ui/icons/Bookmarks";
import ReceiptIcon from "@material-ui/icons/Receipt";
import HelpIcon from "@material-ui/icons/Help";

import TextField from "@material-ui/core/TextField";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import "./row_col.css";
import { FormatAlignCenter } from "../node_modules/@material-ui/icons/index";

import HardwareSetCard from "./components/HardwareSetCard";

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarTitle: {
    flexGrow: 1,
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  appBarItem: {
    marginRight: theme.spacing(2),
  },
  menuButton: {
    marginRight: 36,
  },
  hide: {
    display: "none",
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: "nowrap",
  },
  drawerOpen: {
    width: drawerWidth,
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerClose: {
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: "hidden",
    width: theme.spacing(7) + 1,
    [theme.breakpoints.up("sm")]: {
      width: theme.spacing(9) + 1,
    },
  },
  toolbar: {
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
    height: "100vh",
  },
}));

export default function MiniDrawer() {
  const classes = useStyles();
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  const [auth, setAuth] = React.useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open_prof = Boolean(anchorEl);

  const [open_login, setOpenLogin] = React.useState(false);

  const handleOpenLogin = () => {
    auth ? setAuth(!auth) : setOpenLogin(true);
  };

  const handleCloseLogin = () => {
    setOpenLogin(false);
  };

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleClickLogin = () => {
    setAuth(!auth);
    setOpenLogin(false);
  };

  const handleLogout = () => {
    setAnchorEl(null);
    setAuth(false);
  };

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar
        position="fixed"
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open,
        })}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            className={clsx(classes.menuButton, {
              [classes.hide]: open,
            })}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap className={classes.appBarTitle}>
            UT Compute
          </Typography>
          {auth && (
            <div className={classes.appBarItem}>
              <IconButton
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: "bottom",
                  horizontal: "center",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "bottom",
                  horizontal: "right",
                }}
                open={open_prof}
                onClose={handleClose}
              >
                <MenuItem onClick={handleClose}>Profile</MenuItem>
                <MenuItem onClick={handleClose}>My account</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </div>
          )}
          <div className={classes.appBarItem}>
            <Button
              aria-label="login logout button"
              variant="contained"
              color={auth ? "secondary" : "default"}
              onClick={handleOpenLogin}
            >
              {auth ? "Logout" : "Login"}
            </Button>
            <Dialog
              open={open_login}
              onClose={handleCloseLogin}
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
                  type="text"
                  fullWidth
                />
                <TextField
                  autoFocus
                  margin="dense"
                  id="password"
                  required="true"
                  label="Password"
                  type="password"
                  fullWidth
                />
              </DialogContent>
              <DialogActions>
                <Button onClick={handleCloseLogin} color="primary">
                  Cancel
                </Button>
                <Button onClick={handleClickLogin} color="primary">
                  Login
                </Button>
              </DialogActions>
            </Dialog>
          </div>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        className={clsx(classes.drawer, {
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open,
        })}
        classes={{
          paper: clsx({
            [classes.drawerOpen]: open,
            [classes.drawerClose]: !open,
          }),
        }}
      >
        <div className={classes.toolbar}>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "rtl" ? (
              <ChevronRightIcon />
            ) : (
              <ChevronLeftIcon />
            )}
          </IconButton>
        </div>
        <div>
          <Divider />
          <List>
            <ListItem button key="Hardware Sets">
              <ListItemIcon>
                <DnsRoundedIcon />
              </ListItemIcon>
              <ListItemText primary="Hardware Sets" />
            </ListItem>
            <ListItem button key="Data Sets">
              <ListItemIcon>
                <SettingsEthernetIcon />
              </ListItemIcon>
              <ListItemText primary="Data Sets" />
            </ListItem>
            <ListItem button key="Contact Us">
              <ListItemIcon>
                <HelpIcon />
              </ListItemIcon>
              <ListItemText primary="Contact Us" />
            </ListItem>
          </List>
        </div>
        {auth && (
          <div>
            <Divider />
            <List>
              <ListItem button key="Hardware Set Tickets">
                <ListItemIcon>
                  <ReceiptIcon />
                </ListItemIcon>
                <ListItemText primary="Hardware Set Tickets" />
              </ListItem>
              <ListItem button key="Data Set Bookmarks">
                <ListItemIcon>
                  <BookmarksIcon />
                </ListItemIcon>
                <ListItemText primary="Data Set Bookmarks" />
              </ListItem>
              <ListItem button key="Account">
                <ListItemIcon>
                  <AccountBalanceWalletIcon />
                </ListItemIcon>
                <ListItemText primary="Account" />
              </ListItem>
              <ListItem button key="Dashboard">
                <ListItemIcon>
                  <AssessmentIcon />
                </ListItemIcon>
                <ListItemText primary="Dashboard" />
              </ListItem>
              <ListItem button key="Console">
                <ListItemIcon>
                  <DesktopWindowsIcon />
                </ListItemIcon>
                <ListItemText primary="Console" />
              </ListItem>
            </List>
          </div>
        )}
      </Drawer>
      <main className={classes.content}>
        <div className={classes.toolbar} />
        <div className="row">
          <div className="column">
            <HardwareSetCard
              title="Super Computer - DeepDream"
              description="This is our most powerful compute solution, suitable for longer time
            scales and complex compute tasks"
            />
          </div>
          <div className="column">
            <HardwareSetCard
              title="General Purpose Cloud Computing - PacMan"
              description="These rigs come fully equiped with multicore AMD EPIC
              processors and well and a variety of GPUs to suit your compute
              needs"
            />
          </div>
          <div className="column">
            <HardwareSetCard
              title="Nano Compute - TheTiny"
              description="Your code will run on a raspberry pi module with limited
              resources and compute power"
            />
          </div>
        </div>
      </main>
    </div>
  );
}
