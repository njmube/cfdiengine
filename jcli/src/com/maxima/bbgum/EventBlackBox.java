package com.maxima.bbgum;

class EventBlackBox implements EventElem {

    private final Monitor mon;

    public EventBlackBox(Monitor mon) {
        this.mon = mon;
    }

    public Monitor getMonitor() {
        return this.mon;
    }

    @Override
    public void inComming(EventController v, Action action) {
        v.handlerInComming(this, action);
    }

    @Override
    public void outComming(EventController v, Action action) {
        v.handlerOutComming(this, action);
    }

    @Override
    public void timeOut(EventController v, Action action) {
        v.handlerTimeOut(this, action);
    }

    @Override
    public boolean isFlowTerm(EventController v) {
        return v.handlerIsFlowTerm(this);
    }

    @Override
    public int getConclusion(EventController v) {
        return v.handlerGetConclusion(this);
    }
}
