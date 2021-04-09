import axios from "axios";

const url = "https://ee461l-g11-backend.herokuapp.com/";

export const getHardwareSets = async () => {
  let changeableUrl = `${url}/hardwaresets`;
  try {
    const result = await axios.get(changeableUrl);
    return result.data;
  } catch (error) {
    console.log(error);
  }
};
