import { BrowserRouter, Routes, Route } from "react-router-dom"

const Router = () => {
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<mainPage/>} />
                <Route path="/{id}" element={<mainPage/>} />
            </Routes>
        </BrowserRouter>
    )
}