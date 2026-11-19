import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../auth";

export function RotaProtegida() {
  const { usuario, carregando } = useAuth();
  const local = useLocation();
  if (carregando) return <p style={{ padding: 32 }}>Carregando…</p>;
  if (!usuario) return <Navigate to="/entrar" replace state={{ de: local.pathname + local.search }} />;
  return <Outlet />;
}
