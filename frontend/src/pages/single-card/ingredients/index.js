import styles from "./styles.module.css";

const Ingredients = ({ ingredients, title = "Упражнения" }) => {
  if (!ingredients || !ingredients.length) {
    return null;
  }
  return (
    <div className={styles.ingredients}>
      <h3 className={styles["ingredients__title"]}>{title}:</h3>
      <ul className={styles["ingredients__list"]}>
        {ingredients.map((item) => {
          let line;
          if (item.sets != null && item.reps != null) {
            // Format as "name, X шт." where X = sets × reps
            const totalReps = item.sets * item.reps;
            line = `${item.name}, ${totalReps} шт.`;
          } else if (item.amount) {
            line = `${item.name}, ${item.amount} ${item.measurement_unit || ""}`;
          } else {
            line = item.name;
          }
          const key = `${item.name}-${item.amount}-${item.sets}-${item.reps}`;
          return (
            <li key={key} className={styles["ingredients__list-item"]}>
              {line}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default Ingredients;
