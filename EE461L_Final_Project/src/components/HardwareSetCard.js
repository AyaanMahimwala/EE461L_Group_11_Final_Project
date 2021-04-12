import React from "react";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Flippy, { FrontSide, BackSide } from "react-flippy";

const useStyles = makeStyles((theme) => ({
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    //background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
    height: "50vh",
  },
}));

export default function HardwareSetCard(props) {
  const classes = useStyles();
  return (
    <div className={classes.content}>
      <Flippy
        flipOnHover={true} // default false
        flipOnClick={false} // default false
        flipDirection="horizontal" // horizontal or vertical
        // if you pass isFlipped prop component will be controlled component.
        // and other props, which will go to div
        style={{
          width: "100%",
          height: "100%",
          padding: "20px 10px",
        }} /// these are optional style, it is not necessary
      >
        <FrontSide
          style={{
            backgroundColor: "#41669d",
            position: "absolute",
            width: "100%",
            height: "100%",
            textAlign: "center",
            boxShadow: "0 10px 15px 0 rgba(0,0,0,0.25)",
          }}
          animationDuration="1000"
        >
          <h3
            style={{
              color: "#FFFFFF",
              height: "20%",
            }}
          >
            {props.title}
          </h3>
          <h3
            style={{
              color: "#FFFFFF",
              height: "20%",
            }}
          >
            {props.remaining} remaining units.
          </h3>
        </FrontSide>
        <BackSide
          style={{
            backgroundColor: "#001122",
            position: "absolute",
            width: "100%",
            height: "100%",
            textAlign: "center",
            boxShadow: "0 10px 15px 0 rgba(0,0,0,0.25)",
          }}
          animationDuration="1000"
        >
          <h3
            style={{
              color: "#FFFFFF",
              height: "20%",
            }}
          >
            {props.title}
          </h3>
          <p
            style={{
              color: "#FFFFFF",
              height: "50%",
            }}
          >
            {props.description}
          </p>
          <Button
            aria-label="reserve PacMan"
            variant="contained"
            color="default"
            //onClick={}
          >
            Reserve Details
          </Button>
        </BackSide>
      </Flippy>
    </div>
  );
}
