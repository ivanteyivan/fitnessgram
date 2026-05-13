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
          const line =
            item.sets != null && item.reps != null
              ? `${item.name} — ${item.sets}×${item.reps}${
                  item.measurement_unit ? ` (${item.measurement_unit})` : ""
                }`
              : `${item.name} — ${item.amount} ${item.measurement_unit || ""}`;
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
