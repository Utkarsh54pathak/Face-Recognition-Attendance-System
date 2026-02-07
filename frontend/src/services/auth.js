export const saveAuth = (token, teacher) => {
  localStorage.setItem('token', token);
  localStorage.setItem('teacher', JSON.stringify(teacher));
};

export const getAuth = () => {
  const token = localStorage.getItem('token');
  const teacher = localStorage.getItem('teacher');
  return {
    token,
    teacher: teacher ? JSON.parse(teacher) : null,
  };
};

export const clearAuth = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('teacher');
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};