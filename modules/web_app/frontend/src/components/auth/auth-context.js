import { createContext } from "react"

export const AuthContext = createContext({
    isLoggedIn: false,
    taken: null,
    user: null,
    login: () => { },
    logout: () => { }
})
