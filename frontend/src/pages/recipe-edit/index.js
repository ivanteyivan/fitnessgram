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
import { useParams, useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";
import { Icons } from "../../components";
import cn from "classnames";

const RecipeEdit = ({ onItemDelete }) => {
  const [recipeName, setRecipeName] = useState("");

  const [ingredientValue, setIngredientValue] = useState({
    name: "",
    id: null,
    sets: "",
    reps: "",
    measurement_unit: "",
  });

  const [recipeIngredients, setRecipeIngredients] = useState([]);
  const [recipeText, setRecipeText] = useState("");
  const [recipeTime, setRecipeTime] = useState("");
  const [recipeFile, setRecipeFile] = useState(null);
  const [recipeFileWasManuallyChanged, setRecipeFileWasManuallyChanged] =
    useState(false);

  const [ingredients, setIngredients] = useState([]);
  const [showIngredients, setShowIngredients] = useState(false);
  const [submitError, setSubmitError] = useState({ submitError: "" });
  const [ingredientError, setIngredientError] = useState("");

  const history = useHistory();
  const { id } = useParams();

  const handleAddIngredient = () => {
    if (
      ingredientValue.sets === "" ||
      ingredientValue.reps === "" ||
      !/^\d+$/.test(String(ingredientValue.sets)) ||
      !/^\d+$/.test(String(ingredientValue.reps))
    ) {
      return setIngredientError(
        "Подходы и повторения должны быть целыми числами"
      );
    }
    if (
      Number(ingredientValue.sets) < 1 ||
      Number(ingredientValue.reps) < 1
    ) {
      return setIngredientError("Минимум 1 подход и 1 повторение");
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

    setRecipeIngredients([...recipeIngredients, { ...ingredientValue }]);
    setIngredientValue({
      name: "",
      id: null,
      sets: "",
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

  useEffect(() => {
    api
      .getRecipe({
        recipe_id: id,
      })
      .then((res) => {
        const { image, cooking_time, name, ingredients, text } = res;
        setRecipeText(text);
        setRecipeName(name);
        setRecipeTime(String(cooking_time));
        setRecipeFile(image);
        setRecipeIngredients(ingredients);
      })
      .catch(() => {
        history.push("/recipes");
      });
  }, [id, history]);

  const handleIngredientAutofill = ({ id: exId, name, measurement_unit }) => {
    setIngredientValue({
      ...ingredientValue,
      id: exId,
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
          <title>Редактирование плана — Fitnessgram</title>
          <meta
            name="description"
            content="Fitnessgram — редактирование плана тренировок"
          />
        </MetaTags>
        <Title title="Редактирование тренировочного плана" />
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
                sets: Number(item.sets ?? item.amount ?? 1),
                reps: Number(item.reps ?? 1),
              })),
              cooking_time: recipeTime,
              image: recipeFile,
              recipe_id: id,
            };
            api
              .updateRecipe(data, recipeFileWasManuallyChanged)
              .then(() => {
                history.push(`/recipes/${id}`);
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
            value={recipeName}
            className={styles.mb36}
          />
          <div className={styles.ingredients}>
            <div className={styles.ingredientsInputs}>
              <Input
                label="Упражнения"
                className={styles.ingredientsNameInput}
                inputClassName={styles.ingredientsInput}
                labelClassName={styles.ingredientsLabel}
                placeholder="Начните вводить название"
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
                <p className={styles.amountText}>подходы </p>
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
                      sets: e.target.value,
                    });
                  }}
                  placeholder="3"
                  value={ingredientValue.sets}
                  type="number"
                  min={1}
                />
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
                  onClick={({ id: exId, name, measurement_unit }) => {
                    handleIngredientAutofill({
                      id: exId,
                      name,
                      measurement_unit,
                    });
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
                    key={`${item.id}-${item.sets}-${item.reps}-${item.name}`}
                  >
                    <span className={styles.ingredientsAddedItemTitle}>
                      {item.name}
                    </span>
                    <span> — </span>
                    <span>
                      {item.sets ?? item.amount}×{item.reps ?? ""}
                    </span>
                    {item.measurement_unit ? (
                      <span> ({item.measurement_unit})</span>
                    ) : null}{" "}
                    <span
                      className={styles.ingredientsAddedItemRemove}
                      onClick={() => {
                        setRecipeIngredients(
                          recipeIngredients.filter((ingredient) => {
                            return ingredient.id !== item.id;
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
          <div
            className={cn(
              styles.ingredientsAmountInputContainer,
              styles.ingredientsAmountInputContainerMob
            )}
          >
            <p className={styles.amountText}>подходы </p>
            <Input
              className={styles.ingredientsAmountInput}
              inputClassName={styles.ingredientsAmountValue}
              onChange={(e) => {
                setSubmitError({ submitError: "" });
                setIngredientError("");
                setIngredientValue({
                  ...ingredientValue,
                  sets: e.target.value,
                });
              }}
              placeholder="3"
              value={ingredientValue.sets}
              type="number"
            />
            <p className={styles.amountText}>повторения </p>
            <Input
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
            />
            {ingredientValue.measurement_unit !== "" && (
              <div className={styles.measurementUnit}>
                {ingredientValue.measurement_unit}
              </div>
            )}
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
              placeholder="0"
              value={recipeTime}
            />
            <div className={styles.cookingTimeUnit}>мин.</div>
          </div>
          <Textarea
            label="Описание плана"
            onChange={(e) => {
              setRecipeText(e.target.value);
            }}
            value={recipeText}
            placeholder="Цели, разминка, заметки"
          />
          <FileInput
            onChange={(file) => {
              setRecipeFileWasManuallyChanged(true);
              setRecipeFile(file);
            }}
            fileTypes={["image/png", "image/jpeg"]}
            fileSize={5000}
            className={styles.fileInput}
            label="Загрузить фото плана"
            file={recipeFile}
          />
          <div className={styles.actions}>
            <Button
              modifier="style_dark"
              type="submit"
              className={styles.button}
            >
              Сохранить
            </Button>
            <div
              className={styles.deleteRecipe}
              onClick={() => {
                api.deleteRecipe({ recipe_id: id }).then(() => {
                  onItemDelete && onItemDelete();
                  history.push("/recipes");
                });
              }}
            >
              Удалить план
            </div>
          </div>
          {submitError.submitError && (
            <p className={styles.error}>{submitError.submitError}</p>
          )}
        </Form>
      </Container>
    </Main>
  );
};

export default RecipeEdit;
