import styles from './styles.module.css'

const Description = ({ description, title = "Описание плана" }) => {
  if (!description) {
    return null;
  }
  return (
    <div className={styles.description}>
      <h3 className={styles["description__title"]}>{title}</h3>
      <div className={styles["description__content"]}>{description}</div>
    </div>
  );
};

export default Description

