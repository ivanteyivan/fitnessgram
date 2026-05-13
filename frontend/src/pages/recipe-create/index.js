import {
  Container,
  IngredientsSearch,
  FileInput,
  Input,
  Title,
  Main,
  Form,
  Button,
  Textarea,
} from "../../components";
import styles from "./styles.module.css";
import api from "../../api";
import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";
import { Icons } from "../../components";
import cn from "classnames";

const RecipeCreate = () => {
  const [recipeName, setRecipeName] = useState("");
  const history = useHistory();
  const [ingredientValue, setIngredientValue] = useState({
    name: "",
    id: null,
    sets: 1,
    reps: "",
    measurement_unit: "",
  });
  const [recipeIngredients, setRecipeIngredients] = useState([]);
  const [recipeText, setRecipeText] = useState("");
  const [recipeTime, setRecipeTime] = useState("");
  const [recipeFile, setRecipeFile] = useState(null);

  const [ingredients, setIngredients] = useState([]);
  const [showIngredients, setShowIngredients] = useState(false);
  const [submitError, setSubmitError] = useState({ submitError: "" });
  const [ingredientError, setIngredientError] = useState("");

  const handleAddIngredient = () => {
    if (
      ingredientValue.reps === "" ||
      !/^\d+$/.test(String(ingredientValue.reps))
    ) {
      return setIngredientError("Повторения должны быть целыми числами");
    }
    if (Number(ingredientValue.reps) < 1) {
      return setIngredientError("Минимум 1 повторение");
    }

    if (
      ingredientValue.name === "" ||
      !ingredientValue.id
    ) {
      return setIngredientError("Упражнение не выбрано");
    }

    if (recipeIngredients.find(({ name }) => name === ingredientValue.name)) {
      return setIngredientError("Это упражнение уже добавлено");
    }

    setRecipeIngredients([
      ...recipeIngredients,
      { ...ingredientValue, sets: 1 },
    ]);
    setIngredientValue({
      name: "",
      id: null,
      sets: 1,
      reps: "",
      measurement_unit: "",
    });
  };

  useEffect(() => {
    if (ingredientValue.name === "") {
      return setIngredients([]);
    }
    api.getIngredients({ name: ingredientValue.name }).then((ingredients) => {
      setIngredients(ingredients);
    });
  }, [ingredientValue.name]);

  const handleIngredientAutofill = ({ id, name, measurement_unit }) => {
    setIngredientValue({
      ...ingredientValue,
      id,
      name,
      measurement_unit,
    });
  };

  const checkIfDisabled = () => {
    if (
      recipeText === "" ||
      recipeName === "" ||
      recipeIngredients.length === 0 ||
      recipeTime === "" ||
      recipeFile === "" ||
      recipeFile === null
    ) {
      setSubmitError({ submitError: "Заполните все поля!" });
      return true;
    }

    return false;
  };

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Создание плана — Fitnessgram</title>
          <meta
            name="description"
            content="Fitnessgram — новый план тренировок"
          />
        </MetaTags>
        <Title title="Создание тренировочного плана" />
        <Form
          className={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            if (checkIfDisabled()) {
              return;
            }
            const data = {
              text: recipeText,
              name: recipeName,
              ingredients: recipeIngredients.map((item) => ({
                id: item.id,
                sets: 1,
                reps: Number(item.reps),
              })),
              cooking_time: recipeTime,
              image: recipeFile,
            };
            api
              .createRecipe(data)
              .then((res) => {
                history.push(`/recipes/${res.id}`);
              })
              .catch((err) => {
                const { non_field_errors, exercises, duration } = err;
                if (non_field_errors) {
                  return setSubmitError({
                    submitError: non_field_errors.join(", "),
                  });
                }
                if (exercises) {
                  return setSubmitError({
                    submitError: `Упражнения: ${JSON.stringify(exercises)}`,
                  });
                }
                if (duration) {
                  return setSubmitError({
                    submitError: `Длительность: ${duration[0]}`,
                  });
                }
                const errors = Object.values(err);
                if (errors) {
                  setSubmitError({ submitError: errors.join(", ") });
                }
              });
          }}
        >
          <Input
            label="Название плана"
            onChange={(e) => {
              setSubmitError({ submitError: "" });
              setIngredientError("");
              setRecipeName(e.target.value);
            }}
            className={styles.mb36}
          />
          <div className={styles.ingredients}>
            <div className={styles.ingredientsInputs}>
              <Input
                label="Упражнения"
                className={styles.ingredientsNameInput}
                inputClassName={styles.ingredientsInput}
                placeholder="Начните вводить название"
                labelClassName={styles.ingredientsLabel}
                onChange={(e) => {
                  setSubmitError({ submitError: "" });
                  setIngredientError("");
                  setIngredientValue({
                    ...ingredientValue,
                    name: e.target.value,
                  });
                }}
                onFocus={() => {
                  setShowIngredients(true);
                }}
                value={ingredientValue.name}
              />
              <div className={styles.ingredientsAmountInputContainer}>
                <p className={styles.amountText}>повторения </p>
                <Input
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      handleAddIngredient();
                    }
                  }}
                  className={styles.ingredientsAmountInput}
                  inputClassName={styles.ingredientsAmountValue}
                  onChange={(e) => {
                    setSubmitError({ submitError: "" });
                    setIngredientError("");
                    setIngredientValue({
                      ...ingredientValue,
                      reps: e.target.value,
                    });
                  }}
                  placeholder="12"
                  value={ingredientValue.reps}
                  type="number"
                  min={1}
                />
                {ingredientValue.measurement_unit !== "" && (
                  <div className={styles.measurementUnit}>
                    {ingredientValue.measurement_unit}
                  </div>
                )}
              </div>
              {showIngredients && ingredients.length > 0 && (
                <IngredientsSearch
                  ingredients={ingredients}
                  onClick={({ id, name, measurement_unit }) => {
                    handleIngredientAutofill({ id, name, measurement_unit });
                    setIngredients([]);
                    setShowIngredients(false);
                  }}
                />
              )}
            </div>
            <div className={styles.ingredientAdd} onClick={handleAddIngredient}>
              Добавить упражнение
            </div>
            {ingredientError && (
              <p className={cn(styles.error, styles.errorIngredient)}>
                {ingredientError}
              </p>
            )}
            <div className={styles.ingredientsAdded}>
              {recipeIngredients.map((item) => {
                return (
                  <div
                    className={styles.ingredientsAddedItem}
                    key={`${item.id}-${item.sets}-${item.reps}`}
                  >
                    <span className={styles.ingredientsAddedItemTitle}>
                      {item.name}
                    </span>
                    <span> — </span>
                    <span>
                      {item.reps} повторений
                    </span>
                    {item.measurement_unit ? (
                      <span> ({item.measurement_unit})</span>
                    ) : null}{" "}
                    <span
                      className={styles.ingredientsAddedItemRemove}
                      onClick={() => {
                        setRecipeIngredients(
                          recipeIngredients.filter((ingredient) => {
                            return !(
                              ingredient.id === item.id &&
                              ingredient.sets === item.sets &&
                              ingredient.reps === item.reps
                            );
                          })
                        );
                      }}
                    >
                      <Icons.IngredientDelete />
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
          <div className={styles.cookingTime}>
            <Input
              label="Длительность тренировки"
              className={styles.ingredientsTimeInput}
              labelClassName={styles.cookingTimeLabel}
              inputClassName={styles.ingredientsTimeValue}
              onChange={(e) => {
                setRecipeTime(e.target.value);
              }}
              value={recipeTime}
              placeholder="0"
            />
            <div className={styles.cookingTimeUnit}>мин.</div>
          </div>
          <Textarea
            label="Описание плана"
            onChange={(e) => {
              setRecipeText(e.target.value);
            }}
            placeholder="Цели, разминка, заметки"
          />
          <FileInput
            onChange={(file) => {
              setRecipeFile(file);
            }}
            fileTypes={["image/png", "image/jpeg"]}
            fileSize={5000}
            className={styles.fileInput}
            label="Загрузить фото плана"
          />
          <Button modifier="style_dark" type="submit" className={styles.button}>
            Создать план
          </Button>
          {submitError.submitError && (
            <p className={styles.error}>{submitError.submitError}</p>
          )}
        </Form>
      </Container>
    </Main>
  );
};

export default RecipeCreate;
