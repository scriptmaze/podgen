import React, { useState, useEffect } from "react";
import { useLocation, Link } from "react-router-dom";
import Hamburger from "hamburger-react";
import Podgen from "./Podgen";

const Header = () => {
  // State of our Menu
  const [state, setState] = useState({
    initial: false,
    clicked: null,
    menuName: "Menu",
  });

    const [isOpen, setIsOpen] = useState(false);


  // State of our button
  const [disabled, setDisabled] = useState(false);

  // Get location to listen for route changes
  const location = useLocation();

  // UseEffect to reset the menu state on route change
  useEffect(() => {
    setState({ clicked: false, menuName: "Menu" });
    setIsOpen(false);
  }, [location]);

  // Toggle menu
  const handleMenu = () => {
    disableMenu();
    if (state.initial === false) {
      setState({
        initial: null,
        clicked: true,
        menuName: "Close",
      });
    } else if (state.clicked === true) {
      setState({
        clicked: !state.clicked,
        menuName: "Menu",
      });
    } else if (state.clicked === false) {
      setState({
        clicked: !state.clicked,
        menuName: "Close",
      });
    }
  };

  // Determine if our menu button should be disabled
  const disableMenu = () => {
    setDisabled(!disabled);
    setTimeout(() => {
      setDisabled(false);
    }, 1200);
  };

  return (
    <header>
      <div className="container">
        <div className="wrapper">
          <div className="inner-header">
            <div className="logo">
              <Link to="/">PODGEN.</Link>
            </div>
            <div className="menu">
              <button disabled={disabled} onClick={handleMenu}>
                {/* {state.menuName} */}
                <Hamburger toggled={isOpen} toggle={setIsOpen} />
              </button>
            </div>
          </div>
        </div>
      </div>
      <Podgen state={state} />
    </header>
  );
};

export default Header;
