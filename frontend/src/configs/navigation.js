import Icons from "../components/icons";

export default [
  {
    title: "Тренировочные планы",
    href: "/recipes",
    auth: false,
  },
  {
    title: "Создать план",
    href: "/recipes/create",
    auth: true,
  },
];

export const UserMenu = [
  {
    title: "Мой список тренировок",
    href: "/subscriptions",
    auth: true,
    icon: <Icons.SubscriptionsMenu />,
  },
  {
    title: "Избранное",
    href: "/favorites",
    auth: true,
    icon: <Icons.SavedMenu />,
  },
  {
    title: "Сменить пароль",
    href: "/change-password",
    auth: true,
    icon: <Icons.ResetPasswordMenu />,
  },
];

export const NotLoggedInMenu = [
  {
    title: "Войти",
    href: "/signin",
    auth: false,
  },
  {
    title: "Создать аккаунт",
    href: "/signup",
    auth: false,
  },
];
