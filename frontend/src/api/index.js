class Api {
  constructor(url, headers) {
    this._url = url;
    this._headers = headers;
  }

  checkResponse(res) {
    return new Promise((resolve, reject) => {
      if (res.status === 204) {
        return resolve(res);
      }
      const func = res.status < 400 ? resolve : reject;
      res.json().then((data) => func(data));
    });
  }

  checkFileDownloadResponse(res) {
    return new Promise((resolve, reject) => {
      if (res.status < 400) {
        return res.blob().then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "shopping-list";
          document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
          a.click();
          a.remove(); // afterwards we remove the element again
        });
      }
      reject();
    });
  }

  /** Адаптер: план тренировок → поля карточки «рецепта» во фронте foodgram. */
  _mapWorkoutPlanToRecipeCard(wp) {
    if (!wp) return wp;
    return {
      id: wp.id,
      name: wp.name,
      image: wp.image,
      tags: wp.tags || [],
      author: wp.author || {},
      cooking_time: wp.duration,
      is_favorited: Boolean(wp.is_favorited),
      is_in_shopping_cart: false,
      text: wp.description,
      ingredients: wp.ingredients || [],
    };
  }

  _normalizePaginated(data) {
    if (Array.isArray(data)) {
      return { results: data, count: data.length };
    }
    return {
      results: data.results || [],
      count: data.count ?? (data.results || []).length,
    };
  }

  signin({ email, password }) {
    return fetch("/api/auth/token/login/", {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({
        email,
        password,
      }),
    }).then(this.checkResponse);
  }

  signout() {
    const token = localStorage.getItem("token");
    return fetch("/api/auth/token/logout/", {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  signup({ email, password, username, first_name, last_name }) {
    return fetch(`/api/users/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({
        email,
        password,
        username,
        first_name,
        last_name,
      }),
    }).then(this.checkResponse);
  }

  getUserData() {
    const token = localStorage.getItem("token");
    return fetch(`/api/users/me/`, {
      method: "GET",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  changePassword({ current_password, new_password }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/users/set_password/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
      body: JSON.stringify({ current_password, new_password }),
    }).then(this.checkResponse);
  }

  changeAvatar({ file }) {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("avatar", file);
    return fetch(`/api/users/me/avatar/`, {
      method: "PUT",
      headers: {
        authorization: `Token ${token}`,
      },
      body: formData,
    }).then(this.checkResponse);
  }

  deleteAvatar() {
    const token = localStorage.getItem("token");
    return fetch(`/api/users/me/avatar/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  resetPassword({ email }) {
    return fetch(`/api/users/reset_password/`, {
      method: "POST",
      headers: {
        ...this._headers,
      },
      body: JSON.stringify({ email }),
    }).then(this.checkResponse);
  }

  // «Рецепты» во фронте → планы тренировок на бэкенде

  getRecipes({
    page = 1,
    limit = 6,
    is_favorited = 0,
    is_in_shopping_cart = 0,
    author,
  } = {}) {
    const token = localStorage.getItem("token");
    const authorization = token ? { authorization: `Token ${token}` } : {};
    const params = new URLSearchParams();
    params.set("page", String(page));
    params.set("limit", String(limit));
    if (author) params.set("author", String(author));
    if (is_favorited) params.set("is_favorited", "true");
    return fetch(`/api/workout-plans/?${params.toString()}`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...authorization,
      },
    })
      .then(this.checkResponse)
      .then((data) => {
        const { results, count } = this._normalizePaginated(data);
        return {
          results: results.map((wp) => this._mapWorkoutPlanToRecipeCard(wp)),
          count,
        };
      });
  }

  getRecipe({ recipe_id }) {
    const token = localStorage.getItem("token");
    const authorization = token ? { authorization: `Token ${token}` } : {};
    return fetch(`/api/workout-plans/${recipe_id}/`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...authorization,
      },
    })
      .then(this.checkResponse)
      .then((wp) => this._mapWorkoutPlanToRecipeCard(wp));
  }

  createRecipe() {
    return Promise.reject({
      non_field_errors: [
        "Создание плана через старую форму рецепта не поддерживается.",
      ],
    });
  }

  updateRecipe() {
    return Promise.reject({
      non_field_errors: [
        "Редактирование через старую форму рецепта не поддерживается.",
      ],
    });
  }

  addToFavorites({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/workout-plans/${id}/favorite/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  removeFromFavorites({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/workout-plans/${id}/favorite/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  copyRecipeLink({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/workout-plans/${id}/create_short_link/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    })
      .then(this.checkResponse)
      .then((data) => ({
        "short-link": `${window.location.origin}/recipes/${id}?share=${data.url_hash}`,
      }));
  }

  getUser({ id }) {
    const token = localStorage.getItem("token");
    const authorization = token ? { authorization: `Token ${token}` } : {};
    return fetch(`/api/users/${id}/`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...authorization,
      },
    }).then(this.checkResponse);
  }

  getUsers({ page = 1, limit = 6 }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/users/?page=${page}&limit=${limit}`, {
      method: "GET",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    })
      .then(this.checkResponse)
      .then((data) => this._normalizePaginated(data));
  }

  // subscriptions (в API fitnessgram нет подписок — заглушки)

  getSubscriptions() {
    return Promise.resolve({ results: [], count: 0 });
  }

  deleteSubscriptions() {
    return Promise.resolve({});
  }

  subscribe() {
    return Promise.resolve({});
  }

  // ingredients → упражнения (для автодополнения в старой форме)
  getIngredients({ name }) {
    const token = localStorage.getItem("token");
    const q = name ? `?name=${encodeURIComponent(name)}` : "";
    return fetch(`/api/exercises${q}`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...(token ? { authorization: `Token ${token}` } : {}),
      },
    })
      .then(this.checkResponse)
      .then((data) => {
        const arr = Array.isArray(data) ? data : data.results || [];
        return arr.map((e) => ({
          id: e.id,
          name: e.name,
          measurement_unit: e.muscle_group || "",
        }));
      });
  }

  addToOrders({ id }) {
    return this.addToFavorites({ id });
  }

  removeFromOrders({ id }) {
    return this.removeFromFavorites({ id });
  }

  deleteRecipe({ recipe_id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/workout-plans/${recipe_id}/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  downloadFile() {
    return Promise.reject({
      detail: ["Скачивание списка покупок в fitnessgram не реализовано."],
    });
  }
}

export default new Api(process.env.API_URL || "http://localhost", {
  "content-type": "application/json",
});
