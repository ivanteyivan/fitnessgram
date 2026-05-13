import {
  Card,
  Title,
  Pagination,
  CardList,
  Container,
  Main,
} from "../../components";
import styles from "../favorites/styles.module.css";
import { useRecipes } from "../../utils/index.js";
import { useEffect } from "react";
import api from "../../api";
import MetaTags from "react-meta-tags";

const SubscriptionsPage = ({ updateOrders }) => {
  const {
    recipes,
    setRecipes,
    recipesCount,
    setRecipesCount,
    recipesPage,
    setRecipesPage,
    handleLike,
    handleAddToCart,
  } = useRecipes();

  const loadPlans = ({ page = 1 }) => {
    api
      .getSubscriptions({ page, limit: 6 })
      .then((res) => {
        const { results, count } = res;
        setRecipes(results);
        setRecipesCount(count);
      });
  };

  useEffect(() => {
    loadPlans({ page: recipesPage });
  }, [recipesPage]);

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Мой список тренировок — Fitnessgram</title>
          <meta
            name="description"
            content="Fitnessgram — сохранённые планы тренировок"
          />
        </MetaTags>
        <div className={styles.title}>
          <Title title="Мой список тренировок" />
        </div>
        {recipes.length > 0 && (
          <CardList>
            {recipes.map((card) => (
              <Card
                {...card}
                key={card.id}
                updateOrders={updateOrders}
                handleLike={handleLike}
                handleAddToCart={handleAddToCart}
              />
            ))}
          </CardList>
        )}
        <Pagination
          count={recipesCount}
          limit={6}
          page={recipesPage}
          onPageChange={(page) => setRecipesPage(page)}
        />
      </Container>
    </Main>
  );
};

export default SubscriptionsPage;
