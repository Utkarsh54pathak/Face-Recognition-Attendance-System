import React from 'react';

const ClassCard = ({ classData, onClick }) => (
  <div onClick={onClick} className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer p-6">
    <div className="flex justify-between">
      <div>
        <h3 className="text-xl font-semibold text-gray-900">{classData.name}</h3>
        {classData.subject && <p className="text-sm text-gray-600 mt-1">{classData.subject}</p>}
      </div>
      <div className="text-blue-600 text-2xl">📚</div>
    </div>
    <div className="mt-4 text-sm text-gray-600">
      👥 {classData.student_count} students
    </div>
  </div>
);

export default ClassCard;