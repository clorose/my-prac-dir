// File: C:\_YHJ\fast\frontend\src\components\Header\Header.tsx

import { NavBar, NavLink } from '../../styles/commonStyles';

const Header = () => {
  return (
    <NavBar>
      <NavLink href="/">Main Page</NavLink>
      <NavLink href="/model">Model Viewer</NavLink>
      <NavLink href="/test">Test Cockpit</NavLink>
    </NavBar>
  );
};

export default Header;
