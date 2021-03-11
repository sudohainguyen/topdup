import { useState } from "react"
import "./dup-compare.css"
import DupCompareService from "./dup-compare.service"

const DupCompare = (props) => {
  const [comResults, setComResults] = useState([])
  const [sourceType, setSourceType] = useState('text')
  const [targetType, setTargetType] = useState('text')
  const [sourceText, setSourceText] = useState('')
  const [targetText, setTargetText] = useState('')
  const [sourceUrl, setSourceUrl] = useState('')
  const [targetUrl, setTargetUrl] = useState('')

  const simCheckService = new DupCompareService()

  const getBtnClass = (sourceType, btnLabel) => {
    return sourceType === btnLabel
      ? "layout-cell btn btn-primary btn-sm"
      : "layout-cell btn btn-outline-secondary btn-sm"
  }

  const urlInput = (underlyingValue, setUnderlyingValue) => (
    <form className="full-width margin-horizontal--xs">
      <div className="input-group mb-3">
        <input type="text" className="form-control bg--white" placeholder="URL"
          aria-label="Username" aria-describedby="basic-addon1"
          value={underlyingValue} onChange={($event) => setUnderlyingValue($event.target.value)} />
      </div>
    </form>
  )

  const textInput = (underlyingValue, setUnderlyingValue) => (
    <form className="full-width margin-horizontal--xs">
      <div className="input-group mb-3">
        <textarea type="text" className="form-control bg--white" placeholder="Nội dung"
          aria-label="Username" aria-describedby="basic-addon1" rows={10}
          value={underlyingValue} onChange={($event) => setUnderlyingValue($event.target.value)}>
        </textarea>
      </div>
    </form>
  )

  const sourceContentRenderer = () => {
    return sourceType === 'text'
      ? textInput(sourceText, setSourceText)
      : urlInput(sourceUrl, setSourceUrl)
  }

  const targetContentRenderer = () => {
    return targetType === 'text'
      ? textInput(targetText, setTargetText)
      : urlInput(targetUrl, setTargetUrl)
  }

  const checkSimilarity = () => {
    // TODO: handle url vs url and url vs text
    simCheckService.getSimilarityResults(sourceText, targetText)
      .subscribe(result => {
        setComResults(result.pairs || [])
      })
  }

  const resultsRenderer = () => {
    return comResults.map((item, idx) => (
      <div class="row margin-bottom--xs">
        <div className="col layout-cell">{idx + 1}. {item.source}</div>
        <div className="col layout-cell">{idx + 1}. {item.target}</div>
      </div>
    ))
  }

  return (
    <div className="sim-check-container">
      <div className="layout-grid margin-bottom--20">
        <div className="layout-cell flex-fill sim-check-title">Nhập liên kết hoặc nội dung cần so sánh</div>
        <button type="button" className="btn btn-warning compare-btn" onClick={checkSimilarity}>So sánh</button>
      </div>
      <div className="row">
        <div className="col layout-cell">
          <div className="layout-grid">
            <button type="button" className={getBtnClass(sourceType, 'text')} onClick={() => setSourceType('text')}>Text</button>
            <button type="button" className={getBtnClass(sourceType, 'url')} onClick={() => setSourceType('url')}>URL</button>
          </div>
          <div className="layout-grid">
            {sourceContentRenderer()}
          </div>
        </div>
        <div className="col layout-cell">
          <div className="layout-grid">
            <button type="button" className={getBtnClass(targetType, 'text')} onClick={() => setTargetType('text')}>Text</button>
            <button type="button" className={getBtnClass(targetType, 'url')} onClick={() => setTargetType('url')}>URL</button>
          </div>
          <div className="layout-grid">
            {targetContentRenderer()}
          </div>
        </div>
      </div>
      <div class="full-width margin-bottom--xs">
        <h4>Kết quả: </h4>
        <span>Số cặp trùng {comResults.length}</span>
      </div>
      {resultsRenderer()}
    </div >

  )
}

export default DupCompare

