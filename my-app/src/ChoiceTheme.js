import {styled} from "@mui/system";
import {Button} from "@mui/material";
import { motion } from "framer-motion";
import { useState } from "react";


export const ChoiceButton = styled(Button)({
    display: "inline-block",
    backgroundColor: "#3498db",
    color: "#fff",
    padding: "10px 20px",
    margin: "10px",
    borderRadius: "20px",
    justifyContent: "center",
    transition: "background-color 0.3s",
    '&:hover':{
        backgroundColor: "#2980b9",
    },
});

export const Select = styled("h1")({
    display: 'flex',
    flexDirection: "column",
    alignItems: "center",
    justifyContent: 'center',
})



const variants = {
  checked: { scale: 1.5, rotate: 720, backgroundColor: "#1f75fe" },
  unchecked: { scale: 1, rotate: 0, backgroundColor: "#eee" },
};

export const Checkbox = () => {
    const [isChecked, setChecked] = useState(false);

  return (
    <motion.input
      type="checkbox"
      onChange={(e) => setChecked(e.target.checked)}
      variants={variants}
      initial={false}
      animate={isChecked ? "checked" : "unchecked"}
      style={{
        position: "relative",
        marginRight: "10px",
        width: "24px",
        height: "24px",
        borderRadius: "30px",
        cursor: "pointer",
      }}
      transition={{ duration: 0.5 }}
    />
  );
};