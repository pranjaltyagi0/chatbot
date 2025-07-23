import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface ChatState {
    messages: Message[];
}

const initialState: ChatState = {
    messages: [],
};

const chatSlice = createSlice({
    name: 'chat',
    initialState,
    reducers: {
        sendMessage(state, action: PayloadAction<Message>) {
            state.messages.push(action.payload);
        },
    },
});

export const { sendMessage } = chatSlice.actions;
export default chatSlice.reducer;