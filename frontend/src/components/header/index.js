import styles from "./style.module.css";
import { Nav, AccountMenu, LinkComponent } from "../index.js";
import Container from "../container";

const Header = ({ loggedIn, onSignOut, orders }) => {
  return (
    <header className={styles.header}>
      <Container>
        <div className={styles.headerContent}>
          <LinkComponent
            className={styles.headerLink}
            title={
              <span className={styles.headerBrand} lang="en">
                Fitnessgram
              </span>
            }
            href="/"
          />
          <Nav loggedIn={loggedIn} onSignOut={onSignOut} orders={orders} />
        </div>
      </Container>
    </header>
  );
};

export default Header;
