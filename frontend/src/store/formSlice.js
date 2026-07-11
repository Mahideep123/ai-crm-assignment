import { createSlice } from '@reduxjs/toolkit';
import dayjs from 'dayjs';

const initialState = {
  hcp_name: '',
  interaction_type: 'Meeting',
  date: '',
  time: '',
  attendees: '',
  topics: '',
  materials: '',
  samples: '',
  sentiment: '',
  outcomes: '',
  follow_up: '',
};

const formSlice = createSlice({
  name: 'form',
  initialState,
  reducers: {
    // Full replace – called when a new interaction is logged
    logInteraction: (_state, action) => {
      const payload = { ...action.payload };
      if (!payload.date || payload.date?.toLowerCase().includes('today')) {
        payload.date = dayjs().format('MM/DD/YYYY');
      }
      if (!payload.time) {
        payload.time = dayjs().format('hh:mm A');
      }
      return { ...initialState, ...payload };
    },
    // Partial update – called when editing specific fields
    editInteraction: (state, action) => {
      const payload = { ...action.payload };
      // Resolve "today" if it appears in an edit
      if (payload.date?.toLowerCase().includes('today')) {
        payload.date = dayjs().format('MM/DD/YYYY');
      }
      return { ...state, ...payload };
    },
    resetForm: () => initialState,
  },
});

export const { logInteraction, editInteraction, resetForm } = formSlice.actions;
export default formSlice.reducer;
