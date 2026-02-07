export const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

export const getAttendancePercentage = (present, total) => {
  return total > 0 ? Math.round((present / total) * 100) : 0;
};